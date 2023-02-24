import typing

from pathlib import Path

from pydantic import BaseSettings, Field


ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


class Settings(BaseSettings):
    app_name: str = "SIT - Sports Indoor Tracking "
    admin_email: str = "sven.hoyer@sh-webentwicklung.de"
    password_hash_algorithm: str = Field("bcrypt", env="PASSWORD_HASH_ALGORITHM")
    token_sign_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = Field(..., env="DATABASE_URL")
    db_engine: typing.Any
    project_root: Path = ROOT_DIR
    default_expire_minutes: int = 15

    class Config:
        env_file = ROOT_DIR / "src/config/.env"


settings = Settings()
