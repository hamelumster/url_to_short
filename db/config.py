import os

class DatabaseConfig:
    def __init__(self):
        self.dbname = os.getenv("DBNAME")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")

    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"

db_config = DatabaseConfig()