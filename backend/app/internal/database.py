from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import get_settings
from fastapi import HTTPException

class HTTPObjectNotFound(HTTPException):
    def __init__(self, item: str = "Object") -> None:
        super().__init__(404, f"{item} not found in Database")
        
class HTTPObjectExists(HTTPException):
    def __init__(self) -> None:
        super().__init__(400, "Object already exists in the database")

db_settings = get_settings()
db_url = db_settings.SQLALCHEMY_DATABASE_URL

engine = create_engine(url=db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DB_Base = declarative_base()

