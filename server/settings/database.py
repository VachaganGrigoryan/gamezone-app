from pydantic import Field
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    """Postgres settings."""

    ENGINE: str = 'django.db.backends.postgresql_psycopg2'
    NAME: str = Field('postgres', env="NAME")
    USER: str = Field('postgres', env="USER")
    PASSWORD: str = Field('postgres', env="PASSWORD")
    HOST: str = Field('localhost', env="HOST")
    PORT: str = Field('5432', env="PORT")

    class Config:
        """Config."""
        env_prefix = "DB_"
        case_sensitive = True


class DatabaseSettings(BaseSettings):
    """Database settings."""
    default: PostgresSettings = PostgresSettings()
