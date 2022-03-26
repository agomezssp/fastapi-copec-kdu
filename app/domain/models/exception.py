from json import JSONDecoder
from typing import Optional, List

from pydantic import BaseModel


class Message(BaseModel, JSONDecoder):
    """
    Mensaje de salida para errores
    """
    msg: str
    type: str


class MessageErrorResponse(BaseModel):
    """
    Mensajes de respuesta de los errores
    """
    detail: Optional[List[Message]]

    def __init__(self, msg: str, type: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail = []
        msg = Message(msg=msg, type=type)
        self.detail.append(msg)


class AppException(Exception):
    """
    Errores de la aplicación
    """
    def __init__(
            self,
            message: str,
            type: str,
    ) -> None:
        self.error = MessageErrorResponse(msg=message, type=type)


class NotFoundException(AppException):
    """
    Objecto no encontrado
    """
    def __init__(
            self
    ) -> None:
        super(NotFoundException, self).__init__('No encontrado', 'Not Found')


class ExistsEmailException(AppException):
    """
    El email ya existe
    """
    def __init__(
            self
    ) -> None:
        super(ExistsEmailException, self).__init__('Correo electrónico ya existe registrado', 'Found')
