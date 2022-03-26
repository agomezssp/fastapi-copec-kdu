from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Configuracion de la aplicación
    """

    # Permitir origins en los servicios
    allow_origins: str = '*'

    # Valor del x_api_key a ser comparado por el enviado en el header
    x_api_key: str = 'qwerty'

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
