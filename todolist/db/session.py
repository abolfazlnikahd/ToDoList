from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from todolist.config import DATABASE_URL

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = scoped_session(sessionmaker(bind=engine,
                                           autoflush=False,
                                           autocommit=False, future=True))
