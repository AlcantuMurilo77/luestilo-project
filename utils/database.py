from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from utils.config import Config
from dotenv import load_dotenv

load_dotenv(".env", override=True)

engine = create_engine(Config.url, echo=False)

SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

