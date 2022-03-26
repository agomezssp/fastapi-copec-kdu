from unittest import TestCase

from app.domain.models.exception import AppException, NotFoundException


class TestAppException(TestCase):
    def test_init(self):
        ex = AppException(message='Test', type='type')
        self.assertIsNotNone(ex)
        self.assertEqual('Test', ex.error.detail[0].msg)


class TestNotFoundException(TestCase):
    def test_init(self):
        ex = NotFoundException()
        self.assertIsNotNone(ex)
        self.assertEqual('No encontrado', ex.error.detail[0].msg)
