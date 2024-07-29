from openai import AsyncOpenAI

from api.database.repository.chatbot import get_assistant_by_id, get_thread_by_id
from schemas import QueryCreate

client = AsyncOpenAI()


async def create_and_fill_vector_storage():
    vector_store = await client.beta.vector_stores.create(
        name="Amazon Return Policy",
    )
    files = [open("storage/amazon_policy.json", "rb")]
    file_batch = await client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=files
    )
    return vector_store


async def create_assistant(vector_store):
    assistant = await client.beta.assistants.create(
        name="Amazon Return Policy Assistant",
        instructions="You are amazon customer service. You need to answer customer queries related to the return policy.",
        model="gpt-4o",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    return assistant


async def create_thread():
    thread = await client.beta.threads.create()
    return thread


async def delete_thread(db, thread_id):
    thread = await get_thread_by_id(db, thread_id)
    await client.beta.threads.delete(thread_id=thread.remote_id)


async def create_message(db, thread_id, content):
    assistant = await get_assistant_by_id(db, 1)
    thread = await get_thread_by_id(db, thread_id)
    instructions = """
    Answer the user's query related to the return policy.
    If the user asks a question that is not related to the return policy,
    tell the user to contact Amazon customer service.
    """
    message = await client.beta.threads.messages.create(
        thread_id=thread.remote_id,
        role="user",
        content=content,
    )
    run = await client.beta.threads.runs.create_and_poll(
        thread_id=thread.remote_id,
        assistant_id=assistant.remote_id,
        instructions=instructions,
    )
    if run.status == "completed":
        messages = await client.beta.threads.messages.list(thread_id=thread.remote_id)
        messages = messages.model_dump()["data"]
        response = messages[0]["content"][0]["text"]["value"]

        return QueryCreate(
            query=content,
            response=response,
            thread_id=thread_id,
            **run.model_dump()["usage"],
        )


async def get_messages(db, thread_id):
    thread = await get_thread_by_id(db, thread_id)
    if not thread:
        return []
    messages = await client.beta.threads.messages.list(thread_id=thread.remote_id)
    data = messages.model_dump()["data"]
    return data


async def get_messages_by_remote_id(thread_remot_id):
    messages = await client.beta.threads.messages.list(thread_id=thread_remot_id)
    data = messages.model_dump()["data"]
    return data
