import os
from urllib.parse import quote_plus

def get_database_url() -> str:
    explicit = os.getenv("DATABASE_URL")
    if explicit:
        return explicit

    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "watershed_db")
    user = os.getenv("POSTGRES_USER", "watershed")
    password = quote_plus(os.getenv("POSTGRES_PASSWORD", "watershed_dev_password"))

    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
