from dotenv import load_dotenv
import os 

def test_env_variables_load():
    load_dotenv(".env.test", override=True)
    assert os.getenv("POSTGRES_USER") == "postgres"
    assert os.getenv("POSTGRES_PASS") == "postgres"
    assert os.getenv("POSTGRES_HOST") == "localhost"
    assert os.getenv("POSTGRES_PORT") == "5432"
    assert os.getenv("POSTGRES_DB_NAME") == "test_db"
