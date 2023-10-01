import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    app_env: str = os.environ.get("APP_ENV")
    postgres_db: str = os.environ.get("POSTGRES_DB")
    postgres_user: str = os.environ.get("POSTGRES_USER")
    postgres_password: str = os.environ.get("POSTGRES_PASSWORD")
    postgres_port: int = os.environ.get("POSTGRES_PORT")
    sqlalchemy_database_url: str = (
        f"postgresql+psycopg2://{postgres_user}:{postgres_password}@localhost:"
        f"{postgres_port}/{postgres_db}"
    )
    token: str = os.environ.get("TOKEN")
    weather_api_key: str = os.environ.get("WEATHER_API_KEY")
    news_api_key: str = os.environ.get("NEWS_API_KEY")
    trends_api_key: str = os.environ.get("TRENDS_API_KEY")
    api_secret_key: str = os.environ.get("API_SECRET_KEY")


settings = Settings()
