from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_NAME: str
    
    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    OPENAI_TEXT_EMBEDDING_MODEL: str
    
    MAX_TOKENS: int = 150
    TEMPERATURE: float = 0.5
    
    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()
