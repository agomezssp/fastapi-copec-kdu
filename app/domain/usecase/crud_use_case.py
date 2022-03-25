from typing import List

from ..logics.user_repository import UserRepository
from ..models.exception import ExistsEmailException, NotFoundException
from ..models.user import User, UserCreate


class CrudUseCase:

    def __init__(self, repository: UserRepository):
        self._repository: UserRepository = repository

    def execute_create(self, input_data: UserCreate) -> User:
        user: User = User(**input_data.dict())
        if not self._repository.email_exist(user):
            return self._repository.create(input_data)
        else:
            raise ExistsEmailException()

    def execute_update(self, input_data: User) -> User:
        if self._repository.email_exist(input_data):
            raise ExistsEmailException()
        result = self._repository.update(input_data)
        if result is None:
            raise NotFoundException()
        return result

    def execute_detail(self, user_id: str) -> User:
        user = self._repository.detail(user_id)
        if user is None:
            raise NotFoundException()
        return user

    def execute_all(self) -> List[User]:
        return self._repository.list()

    def execute_delete(self, user_id: str) -> None:
        user = self._repository.delete(user_id)
        if user is None:
            raise NotFoundException()
