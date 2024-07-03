import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for SQLAlchemy")

engine = create_engine(DATABASE_URL)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
