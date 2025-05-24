from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/api")

try:
    with engine.connect() as conn:
        print("Connected!")
except Exception as e:
    print("Error:")
    print(e)