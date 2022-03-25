from json import JSONDecoder

from pydantic import BaseModel


class MessageErrorResponse(BaseModel, JSONDecoder):
    msg: str
    type: str


class AppException(Exception):
    def __init__(
            self,
            message: str,
            type: str,
    ) -> None:
        self.error = MessageErrorResponse(msg=message, type=type)


class NotFoundException(AppException):
    def __init__(
            self
    ) -> None:
        super(NotFoundException, self).__init__('No encontrado', 'Not Found')


class ExistsEmailException(AppException):
    def __init__(
            self
    ) -> None:
        super(ExistsEmailException, self).__init__('Correo electrónico ya existe registrado', 'Found')
