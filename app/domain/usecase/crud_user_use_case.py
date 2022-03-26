from typing import List

from ..logics.user_repository import UserRepository
from ..models.exception import ExistsEmailException, NotFoundException
from ..models.user import User, UserCreate


class CrudUserUseCase:
    """
    Caso de uso de operaciones de usuario.
    """

    def __init__(self, repository: UserRepository):
        """
        :param repository: Repositorio de usuarios
        """
        self._repository: UserRepository = repository

    def execute_create(self, input_data: UserCreate) -> User:
        """
        Crear nuevo usuario si el email no existe. General el Id automáticamente
        :param input_data: Datos del usuario a ser creado
        :return: Usuario creado con el ID generado
        :exception ExistsEmailException si el email ya existe en la lista de usuarios
        """
        user: User = User(**input_data.dict())
        if not self._repository.email_exist(user):
            return self._repository.create(input_data)
        else:
            raise ExistsEmailException()

    def execute_update(self, input_data: User) -> User:
        """
        Actualiza los datos de un usuario.
        :param input_data: Usuario a ser actualizado
        :return: El usuario actualizado
        :exception NotFoundException si no se encuentra
        :exception ExistsEmailException si se cambia el email este ya existe en la lista
        """
        index = self._repository.find(str(input_data.id))
        if index < 0:
            raise NotFoundException()
        if self._repository.email_exist(input_data):
            raise ExistsEmailException()
        result = self._repository.update(input_data)
        if result is None:
            raise NotFoundException()
        return result

    def execute_detail(self, user_id: str) -> User:
        """
        Obtener un usuario
        :param user_id: Id del usuario a obtener
        :return: Usuario encontrado
        :exception NotFoundException si no se encuentra
        """
        user = self._repository.detail(user_id)
        if user is None:
            raise NotFoundException()
        return user

    def execute_all(self) -> List[User]:
        """
        Obtener a lista de todos los usuarios
        :return: Lista de usuarios
        """
        return self._repository.list()

    def execute_delete(self, user_id: str) -> None:
        """
        Elimina un usuario
        :param user_id: ID del usuario a eliminar
        :exception NotFoundException si no se encuentra
        """
        user = self._repository.delete(user_id)
        if user is None:
            raise NotFoundException()
