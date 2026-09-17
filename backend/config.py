import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv(
        "APP_NAME",
        "BTIP - Business Turnaround Intelligence Platform"
    )

    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/btip"
    )

    DEBUG = os.getenv("DEBUG", "True").lower() == "true"


settings = Settings()