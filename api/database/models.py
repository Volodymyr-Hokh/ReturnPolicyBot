from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    BigInteger,
)
from sqlalchemy.orm import relationship

from api.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)

    threads = relationship("Thread", back_populates="user")


class Assistant(Base):
    __tablename__ = "assistants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    instructions = Column(String, nullable=True)
    remote_id = Column(String, nullable=False)
    vector_storage_id = Column(String, nullable=False)

    threads = relationship("Thread", back_populates="assistant")


class Thread(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    remote_id = Column(String, nullable=False)
    assistant_id = Column(
        Integer, ForeignKey("assistants.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime, nullable=False)

    queries = relationship(
        "Query", back_populates="thread", cascade="all, delete-orphan"
    )

    assistant = relationship("Assistant", back_populates="threads")
    user = relationship("User", back_populates="threads")


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, nullable=False)
    response = Column(String, nullable=False)
    completion_tokens = Column(Integer, nullable=False)
    prompt_tokens = Column(Integer, nullable=False)
    total_tokens = Column(Integer, nullable=False)
    thread_id = Column(
        Integer, ForeignKey("threads.id", ondelete="CASCADE"), nullable=False
    )

    thread = relationship("Thread", back_populates="queries")
