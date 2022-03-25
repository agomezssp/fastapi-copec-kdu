import uuid
from unittest import TestCase

from app.domain.models.exception import ExistsEmailException, NotFoundException
from app.domain.models.user import UserCreate
from app.domain.usecase.crud_use_case import CrudUseCase
from app.repository.user_repository_in_memory_impl import UserRepositoryInMemoryImpl


class TestCrudUseCase(TestCase):
    def setUp(self):
        self.user_data = {
            'name': 'UserName',
            'email': 'email@email.com',
            'birth_date': '2000-10-02',
            'lastname': 'UserLastName'
        }

    def test_execute_create(self):
        repo = UserRepositoryInMemoryImpl()
        repo.delete_all()
        use_case = CrudUseCase(repository=repo)

        user: UserCreate = UserCreate(**self.user_data)
        user_created = use_case.execute_create(user)
        self.assertEqual(user.name, user_created.name)
        self.assertIsNotNone(user_created.id)
        user2 = UserCreate(**self.user_data)
        user2.email = 'another.ameil@email.com'
        user_created = use_case.execute_create(user2)
        self.assertEqual(user2.email, user_created.email)
        self.assertIsNotNone(user_created.id)
        with self.assertRaises(ExistsEmailException):
            use_case.execute_create(user)

    def test_execute_update(self):
        repo = UserRepositoryInMemoryImpl()
        repo.delete_all()
        use_case = CrudUseCase(repository=repo)

        user: UserCreate = UserCreate(**self.user_data)
        user_created = use_case.execute_create(user).copy()
        user_created.name = 'OtherName'
        user_created.email = 'another.ameil@email.com'
        user_update = use_case.execute_update(user_created)
        self.assertEqual('OtherName', user_update.name)
        self.assertEqual(user_created.id, user_update.id)
        user_not_found = user_update.copy()
        user_not_found.id = uuid.uuid1()
        with self.assertRaises(ExistsEmailException):
            use_case.execute_update(user_not_found)
        user_not_found.email = 'new@email.com'
        with self.assertRaises(NotFoundException):
            use_case.execute_update(user_not_found)

    def test_execute_detail(self):
        repo = UserRepositoryInMemoryImpl()
        repo.delete_all()
        use_case = CrudUseCase(repository=repo)

        user: UserCreate = UserCreate(**self.user_data)
        user_created = use_case.execute_create(user).copy()
        user_detail = use_case.execute_detail(str(user_created.id))
        self.assertEqual(user_created.id, user_detail.id)

    def test_execute_all(self):
        repo = UserRepositoryInMemoryImpl()
        repo.delete_all()
        use_case = CrudUseCase(repository=repo)

        user: UserCreate = UserCreate(**self.user_data)
        use_case.execute_create(user)
        user2: UserCreate = UserCreate(**self.user_data)
        user2.email = 'new@email.com'
        use_case.execute_create(user2)
        users = use_case.execute_all()
        self.assertEqual(2, len(users))

    def test_execute_delete(self):
        repo = UserRepositoryInMemoryImpl()
        repo.delete_all()
        use_case = CrudUseCase(repository=repo)

        user: UserCreate = UserCreate(**self.user_data)
        user_created = use_case.execute_create(user)
        use_case.execute_delete(str(user_created.id))
        with self.assertRaises(NotFoundException):
            use_case.execute_delete(str(uuid.uuid4()))
