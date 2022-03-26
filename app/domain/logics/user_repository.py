from abc import ABC, abstractmethod
from typing import List

from ..models.user import User, UserCreate


class UserRepository(ABC):
    """
    Respositorio de operaciones de usuario
    """

    @abstractmethod
    def create(self, user: UserCreate) -> User:
        """
        Crear el usuario
        :param user: Datos del usuario
        :return: Datos del usuario creado
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> User:
        """
        Actualizar datos del usuario segun su ID
        :param user: usuario.
        :return: usuario actualizado o None si no se encuentra
        """
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[User]:
        """
        Listado de todos los usuarios creados
        :return: Listado de usuarios
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str) -> None:
        """
        Busca y elimina un usuario
        :param id: ID del usuario a ser eliminado
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def delete_all(self) -> None:
        """
        Eliminar todos los usarios del listado
        """
        raise NotImplementedError

    @abstractmethod
    def detail(self, id: str) -> User:
        """
        Obtener un usuario
        :param id: ID del usuario
        :return: Usuario o None
        """
        raise NotImplementedError

    @abstractmethod
    def email_exist(self, user_check: User):
        """
        Chequea en la lista de usuario que el email exista para todos los usuario diferentes al que se quiere chequear
        :param user_check:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def find(self, user_id: str) -> int:
        """
        Busca en el listado de usuario el índice correspondiente al mismo segun su ID
        :param user_id: id del usuario a buscar
        :return: indice del usuario. -1 si no lo encuentra
        """
        raise NotImplementedError
