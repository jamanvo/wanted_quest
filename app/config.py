import os


class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    PROJECT_NAME = "Wanted Queat"


settings = Settings()
