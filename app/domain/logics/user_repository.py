from abc import ABC, abstractmethod
from typing import List

from ..models.user import User, UserCreate


class UserRepository(ABC):

    @abstractmethod
    def create(self, user: UserCreate) -> User:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_all(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def detail(self, id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def email_exist(self, user_check: User):
        raise NotImplementedError
