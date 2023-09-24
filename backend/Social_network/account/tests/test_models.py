from faker import Faker
from django.test import TestCase

fake = Faker()


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
