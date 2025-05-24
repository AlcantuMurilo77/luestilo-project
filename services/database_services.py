from sqlalchemy import create_engine
from utils.config import Config
from dotenv import load_dotenv

load_dotenv(".env", override=True)

class DatabaseRepository():

    def __init__(self, connection_string):

        self.engine = create_engine(connection_string)

global_db_repository = DatabaseRepository(Config.url)
