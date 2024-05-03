from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from pydantic_settings import BaseSettings

class DB_Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str

    class Config:
        env_file = "app/.env"

db_settings = DB_Settings()
db_url = db_settings.SQLALCHEMY_DATABASE_URL

engine = create_engine(url=db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DB_Base = declarative_base()

