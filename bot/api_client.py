import aiohttp

from config import settings
from schemas import (
    MessageCreate,
    MessageResponse,
    AssistantResponse,
    ThreadCreate,
    ThreadResponse,
    UserCreate,
    UserResponse,
)


class APIClient:

    def __init__(self):
        self.base_url = settings.api_base_url
        self.session = None

    async def __aenter__(self):
        self.session = await aiohttp.ClientSession().__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.__aexit__(exc_type, exc, tb)

    async def create_assistant(self) -> AssistantResponse:
        async with self.session.post(f"{self.base_url}/chat/assistant") as response:
            data = await response.json()
            if response.status != 201:
                return {"error": data}
            return AssistantResponse(**data)

    async def create_thread(self, telegram_id: int) -> ThreadResponse:
        async with self.session.post(
            f"{self.base_url}/chat/thread", params={"telegram_id": telegram_id}
        ) as response:
            res = await response.json()
            print(res)
            return ThreadResponse(**res)

    async def get_thread_by_user_telegram_id(self, telegram_id: int) -> ThreadResponse:
        async with self.session.get(
            f"{self.base_url}/chat/thread/{telegram_id}"
        ) as response:
            return ThreadResponse(**await response.json())

    async def delete_thread(self, thread_id: int) -> None:
        async with self.session.delete(
            f"{self.base_url}/chat/thread/{thread_id}"
        ) as response:
            return response.status

    async def delete_all_user_threads(self, user_telegram_id: int) -> None:
        async with self.session.delete(
            f"{self.base_url}/chat/threads/{user_telegram_id}"
        ) as response:
            return response.status

    async def create_message(self, message: MessageCreate) -> MessageResponse:
        async with self.session.post(
            f"{self.base_url}/chat/message", json=message.model_dump()
        ) as response:
            res = await response.json()
            return res.get("response", "Something went wrong. Please try again later.")

    async def create_user(self, user: UserCreate) -> UserResponse:
        async with self.session.post(
            f"{self.base_url}/users", json=user.model_dump()
        ) as response:
            if response.status == 400:
                return {"message": "User already exists"}
            return UserResponse(**await response.json())

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserResponse:
        async with self.session.get(
            f"{self.base_url}/users/telegram/{telegram_id}"
        ) as response:
            return UserResponse(**await response.json())

    async def delete_user(self, user_id: int) -> None:
        async with self.session.delete(f"{self.base_url}/users/{user_id}") as response:
            return response.status


async def create_api_client() -> APIClient:
    return APIClient()
