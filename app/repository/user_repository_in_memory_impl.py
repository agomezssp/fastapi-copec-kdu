from typing import List, Optional

from ..domain.logics.user_repository import UserRepository
from ..domain.models.user import User, UserCreate


class UserRepositoryInMemoryImpl(UserRepository):
    users: List[User] = []

    def create(self, user: UserCreate) -> User:
        user: User = User(**user.dict())
        self.users.append(user)
        return user

    def update(self, user: User) -> Optional[User]:
        index = self.find(str(user.id))
        if index >= 0:
            self.users[index] = user
            return user
        else:
            return None

    def list(self) -> List[User]:
        return self.users

    def delete(self, user_id: str) -> Optional[User]:
        index = self.find(str(user_id))
        if index >= 0:
            user = self.users[index]
            del self.users[index]
            return user
        else:
            return None

    def delete_all(self) -> None:
        self.users = []

    def detail(self, user_id: str) -> User:
        return next(filter(lambda user: str(user.id) == user_id, self.users), None)

    def email_exist(self, user_check: User):
        return next(filter(
            lambda user: user.email == user_check.email and user.id != user_check.id, self.users
        ), None) is not None

    def find(self, user_id: str) -> int:
        """
        :rtype: int
        """
        try:
            return next(index for (index, u) in enumerate(self.users) if str(u.id) == user_id)
        except StopIteration as err:
            return -1

