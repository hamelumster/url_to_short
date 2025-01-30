import os

from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.dbname = os.getenv("DBNAME")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.host = os.getenv("HOST") or "localhost"
        self.port = os.getenv("PORT") or "5432"

    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"

db_config = DatabaseConfig()