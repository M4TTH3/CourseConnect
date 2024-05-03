from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from .settings import get_settings

db_settings = get_settings()
db_url = db_settings.SQLALCHEMY_DATABASE_URL

engine = create_engine(url=db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DB_Base = declarative_base()

