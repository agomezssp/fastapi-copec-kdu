from pydantic import BaseSettings


class Settings(BaseSettings):
    allow_origins: str = '*'
    x_api_key: str = 'qwerty'  # TODO

    class Config:
        env_file = ".env"
