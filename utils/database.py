from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from utils.config import Config
from dotenv import load_dotenv

load_dotenv(".env", override=True)

try:
    engine = create_engine(Config.url, echo=False)

    with engine.connect() as connection:
        connection.execute("SELECT 1")
    
    SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

except SQLAlchemyError as e:
    raise RuntimeError(f"[DB ERROR] Error conecting to PostgresDB: {e}")
except Exception as e:
    raise RuntimeError(f"[UNEXPECTED ERROR] Unexpected error on initializing engie: {e}")