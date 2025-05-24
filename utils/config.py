import os





class Config:
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASS")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB_NAME")
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
