from django.test import TestCase

from user.models import Tier, User
from user.serializer import LoginUserSerializer, UserSerializer


class LoginUserTestCase(TestCase):
    def setUp(self):
        self.account = {
            "username": "admin",
            "password": "qwerty",
        }

        self.user = User.objects.create_user(**self.account)
        self.serializer = LoginUserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["username"]))

    def test_username_field_content(self):
        data = self.serializer.data

        self.assertEqual(data["username"], self.account["username"])


class UserTestCase(TestCase):
    def setUp(self):
        self.account = {
            "username": "admin",
            "password": "qwerty",
            "email": "admin@damin.com",
            "image_tier": Tier.objects.create(name="Premium"),
        }

        self.user = User.objects.create_user(**self.account)
        self.serializer = UserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["id", "email", "image_tier"]))

    def test_email_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["email"], self.account["email"])

    def test_id_field_content(self):
        data = self.serializer.data
        self.assertTrue(data["id"])

    def test_image_tier_field_content(self):
        data = self.serializer.data
        self.assertTrue(data["image_tier"])
