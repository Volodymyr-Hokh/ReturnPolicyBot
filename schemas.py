from datetime import date, datetime
import re
from typing import List, Optional, Any, Dict


from pydantic import BaseModel, ConfigDict


########################USER SCHEMAS########################
class UserCreate(BaseModel):
    username: Optional[str] = None
    telegram_id: int


class UserInDB(UserCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: int
    username: Optional[str] = None
    telegram_id: int

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    telegram_id: Optional[int] = None


########################CHATBOT SCHEMAS########################


class MessageCreate(BaseModel):
    content: str
    thread_id: int


class MessageText(BaseModel):
    annotations: List[Any]
    value: str


class MessageContent(BaseModel):
    text: MessageText
    type: str


class MessageResponse(BaseModel):
    id: str
    assistant_id: Optional[str] = None
    attachments: List
    completed_at: Optional[str]
    content: List[MessageContent]
    created_at: int
    incomplete_at: Optional[str]
    incomplete_details: Optional[Any]
    metadata: Dict[str, Any]
    object: str
    role: str
    run_id: Optional[str] = None
    status: Optional[str]
    thread_id: str


class AssistantCreate(BaseModel):
    name: str
    instructions: str
    remote_id: str
    vector_storage_id: str


class AssistantResponse(AssistantCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ThreadCreate(BaseModel):
    name: Optional[str] = None
    remote_id: str
    assistant_id: int
    user_id: int
    created_at: datetime = datetime.now()


class ThreadResponse(ThreadCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class QueryCreate(BaseModel):
    query: str
    response: str
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    thread_id: int


class QueryResponse(QueryCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
