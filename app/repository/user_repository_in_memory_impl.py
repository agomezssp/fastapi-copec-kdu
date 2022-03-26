import logging

from typing import List, Optional

from ..domain.logics.user_repository import UserRepository
from ..domain.models.user import User, UserCreate

logger = logging.getLogger(__name__)


class UserRepositoryInMemoryImpl(UserRepository):
    """
    Respositorio de operaciones de usuario
    """
    users: List[User] = []

    def create(self, user: UserCreate) -> User:
        """
        Crear el usuario
        :param user: Datos del usuario
        :return: Datos del usuario creado
        """
        logger.debug(f'Creación de usuario solicitada: {user.dict()}')
        user: User = User(**user.dict())
        self.users.append(user)
        logger.info(f'Usuario creado ID={user.id}')
        return user

    def update(self, user: User) -> Optional[User]:
        """
        Actualizar datos del usuario segun su ID
        :param user: usuario.
        :return: usuario actualizado o None si no se encuentra
        """
        logger.debug(f'Actualización de usuario solicitada: {user.dict()}')
        index = self.find(str(user.id))
        if index >= 0:
            self.users[index] = user
            logger.info(f'Usuario actualizado ID={user.id}')
            return user
        logger.error(f'No existe el usuario ID={user.id}')
        return None

    def list(self) -> List[User]:
        """
        Listado de todos los usuarios creados
        :return: Listado de usuarios
        """
        logger.info('Listando usuarios')
        return self.users

    def delete(self, user_id: str) -> Optional[User]:
        """
        Busca y elimina un usuario
        :param user_id: ID del usuario a ser eliminado
        :return:
        """
        index = self.find(str(user_id))
        if index >= 0:
            user = self.users[index]
            del self.users[index]
            return user
        return None

    def delete_all(self) -> None:
        """
        Eliminar todos los usarios del listado
        """
        self.users = []

    def detail(self, user_id: str) -> User:
        """
        Obtener un usuario
        :param user_id: ID del usuario
        :return: Usuario o None
        """
        return next(filter(lambda user: str(user.id) == user_id, self.users), None)

    def email_exist(self, user_check: User) -> bool:
        """
        Chequea en la lista de usuario que el email exista para todos los usuario diferentes al que se quiere chequear
        :param user_check:
        :return: bool si ya hay un usuario con ese email o no
        """
        return next(filter(
            lambda user: user.email == user_check.email and user.id != user_check.id, self.users
        ), None) is not None

    def find(self, user_id: str) -> int:
        """
        Busca en el listado de usuario el índice correspondiente al mismo segun su ID
        :param user_id:
        :return: indice del usuario
        """
        try:

            return next(index for (index, u) in enumerate(self.users) if str(u.id) == user_id)
        except StopIteration as err:
            return -1
