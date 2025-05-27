from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from utils.config import Config

# for attempt in range(1, MAX_RETRIES + 1):
try:
    engine = create_engine(Config.url, echo=False)
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))
    print("[DB] Connected successfully.")
except Exception as e:
    raise RuntimeError(f"[UNEXPECTED ERROR] {e}")
# else:
#     raise RuntimeError("[DB ERROR] Could not connect to the database after several attempts.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
