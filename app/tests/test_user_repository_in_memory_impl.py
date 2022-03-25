import uuid
from unittest import TestCase

from app.domain.models.user import UserCreate
from app.repository.user_repository_in_memory_impl import UserRepositoryInMemoryImpl


class TestUserRepositoryInMemoryImpl(TestCase):
    def setUp(self):
        self.repository = UserRepositoryInMemoryImpl()
        self.user_data = {
            'name': 'UserName',
            'email': 'email@email.com',
            'birth_date': '2000-10-02',
            'lastname': 'UserLastName'
        }

    def test_create(self):
        self.repository.delete_all()
        user: UserCreate = UserCreate(**self.user_data)
        user_created = self.repository.create(user)
        self.assertEqual(user.name, user_created.name)
        self.assertIsNotNone(user_created.id)

    def test_update(self):
        self.repository.delete_all()
        user: UserCreate = UserCreate(**self.user_data)
        user_created = self.repository.create(user).copy()
        user_created.name = 'OtherName'
        user_update = self.repository.update(user_created)
        self.assertEqual('OtherName', user_update.name)
        self.assertEqual(user_created.id, user_update.id)
        user_not_found = user_update.copy()
        user_not_found.id = uuid.uuid1()
        self.assertIsNone(self.repository.update(user_not_found))

    def test_list(self):
        self.repository.delete_all()
        user: UserCreate = UserCreate(**self.user_data)
        self.repository.create(user)
        self.repository.create(user)
        self.repository.create(user)
        users = self.repository.list()
        self.assertEqual(3, len(users))

    def test_delete(self):
        self.repository.delete_all()
        user: UserCreate = UserCreate(**self.user_data)
        self.repository.create(user)
        user2 = self.repository.create(user)
        self.repository.create(user)
        self.repository.delete(str(user2.id))
        users = self.repository.list()
        self.assertEqual(2, len(users))
        self.assertIsNone(self.repository.delete(str(user2.id)))

    def test_detail(self):
        self.repository.delete_all()
        user: UserCreate = UserCreate(**self.user_data)
        self.repository.create(user)
        user2 = self.repository.create(user)
        self.repository.create(user)
        user4 = self.repository.create(user)
        users = self.repository.list()
        self.assertEqual(4, len(users))

        self.assertEqual(user2, self.repository.detail(str(user2.id)))
        self.assertEqual(user4, self.repository.detail(str(user4.id)))
        self.assertIsNone(self.repository.detail(uuid.uuid1().__str__()))
