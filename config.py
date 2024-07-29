from dotenv import load_dotenv
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    jwt_secret_key: str
    jwt_algorithm: str

    telegram_bot_token: str

    api_base_url: str

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


settings = Settings()
