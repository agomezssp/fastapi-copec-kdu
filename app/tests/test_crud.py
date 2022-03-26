import datetime
import uuid

from fastapi.testclient import TestClient
from starlette import status

from app.dependencies import get_settings
from app.domain.models.user import User
from app.main import app
from unittest import TestCase

headers = {"X-Api-Key": get_settings().x_api_key}


class Test(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.route_prefix = "/api/v1/user"

    def test_create(self):
        response = self.client.post(f'{self.route_prefix}/', headers=headers, json={
            "name": "Juan",
            "lastname": "Perez Montes",
            "email": "email@mail.com",
            "birth_date": "2000-10-20"
        })
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIsNotNone(response.json())

        # Testing not X-Api-Key
        response = self.client.post(f'{self.route_prefix}/', json={})
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        # Testing not X-Api-Key
        response = self.client.post(f'{self.route_prefix}/', headers={"X-Api-Key": '1234'}, json={})
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_all(self):
        response = self.client.get(f'{self.route_prefix}/', headers=headers)
        print(response.json())
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_validation_error(self):
        # Testing create user
        response = self.client.post(f'{self.route_prefix}/', headers=headers, json={
            "name": "",
            "lastname": "Perez Montes_2",
            "email": "invalid",
            "birth_date": "2000-10-22"
        })
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)

        # Testing update user
        response = self.client.put(f'{self.route_prefix}/', headers=headers , json={
            "lastname": "Perez Montes_2",
            "email": "invalid",
            "birth_date": ""
        })
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)

        # Testing create user
        response = self.client.post(f'{self.route_prefix}/', headers=headers, json={})
        print(response.json())
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)

    def test_all_methods(self):
        # Testing create user
        response_user = self.client.post(f'{self.route_prefix}/', headers=headers, json={
            "name": "Juan_2",
            "lastname": "Perez Montes_2",
            "email": "email.2@mail.com",
            "birth_date": "2000-10-22"
        })
        self.assertEqual(status.HTTP_201_CREATED, response_user.status_code)
        user: User = User(**response_user.json())
        user_id = user.id
        # Testing ExistsEmailException
        response_user = self.client.post(f'{self.route_prefix}/', headers=headers, json={
            "name": "Juan_2",
            "lastname": "Perez Montes_2",
            "email": "email.2@mail.com",
            "birth_date": "2000-10-22"
        })
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response_user.status_code)
        print(response_user.json())

        # Testing Update user
        response = self.client.put(f'{self.route_prefix}/', headers=headers, json={
            "name": "Juan_3",
            "lastname": "Perez Montes_3",
            "email": "email.3@mail.com",
            "birth_date": "2000-10-20",
            "id": str(user_id)
        })
        user_updated: User = User(**response.json())
        self.assertEqual('Juan_3', user_updated.name)
        self.assertEqual(datetime.date(year=2000, month=10, day=20), user_updated.birth_date)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Test update the same user
        response = self.client.put(f'{self.route_prefix}/', headers=headers, json={
            "name": "Juan_3",
            "lastname": "Perez Montes_3",
            "email": "email.3@mail.com",
            "birth_date": "2000-10-21",
            "id": str(user_id)
        })
        user_updated: User = User(**response.json())
        self.assertEqual('Juan_3', user_updated.name)
        self.assertEqual(datetime.date(year=2000, month=10, day=21), user_updated.birth_date)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Test get One User
        response_detail = self.client.get(f'{self.route_prefix}/{user_id}', headers=headers)
        self.assertEqual(status.HTTP_200_OK, response_detail.status_code)
        self.assertIsNotNone(response.json()['id'])
        # Not Found
        response_detail = self.client.get(f'{self.route_prefix}/{str(uuid.uuid4())}', headers=headers)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response_detail.status_code)

        # Test Delete
        response_delete = self.client.delete(f'{self.route_prefix}/{user_id}', headers=headers)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response_delete.status_code)
        # Test Delete Not Found
        response_delete = self.client.delete(f'{self.route_prefix}/{str(uuid.uuid4())}', headers=headers)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response_delete.status_code)
