
from dotenv import load_dotenv
load_dotenv(".env.test", override=True)
import pytest
from sqlalchemy.orm import sessionmaker
from utils.database import engine
from models.models import Base


TestingSessionLocal = sessionmaker(bind=engine,
                                   autoflush=False,
                                   autocommit=False)

@pytest.fixture(scope="function")
def db():
    print(engine.url)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

