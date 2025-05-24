import os 
import sys
from dotenv import load_dotenv
from sqlalchemy import text
load_dotenv(".env.test", override=True)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from utils.config import Config

from services.database_services import DatabaseRepository

def test_database_connection():
    engine = DatabaseRepository(Config.url).engine
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except Exception as e:
        assert False, f"Error: {e}"
