from django.http import HttpRequest
from django.test import TestCase
from freezegun import freeze_time
from rest_framework.exceptions import AuthenticationFailed

from user.authentication import CustomUserAuthentication
from user.models import User

request = HttpRequest()


class AuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin", password="qwerty", id=1)

    @freeze_time("2023-02-28")
    def test_authenticate_good_time(self):
        request = HttpRequest()
        request.COOKIES[
            "jwt"
        ] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNjc3NjEyOTc2LCJpYXQiOjE2Nzc1MjY1NzZ9.yiONgsuT9bxgVml3Lxw4bS0Ho_qgLyYDKKVLzz9G4iI"

        user = CustomUserAuthentication().authenticate(request)

        self.assertEqual(user, (self.user, None))

    @freeze_time("2024-02-28")
    def test_authenticate_expired(self):
        request = HttpRequest()
        request.COOKIES[
            "jwt"
        ] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNjc3NjEyOTc2LCJpYXQiOjE2Nzc1MjY1NzZ9.yiONgsuT9bxgVml3Lxw4bS0Ho_qgLyYDKKVLzz9G4iI"

        with self.assertRaises(AuthenticationFailed):
            CustomUserAuthentication().authenticate(request)

    @freeze_time("2024-02-28")
    def test_authenticate_bad(self):
        request = HttpRequest()
        request.COOKIES[
            "jwt"
        ] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxdc3NjEyOTc2LCJpYXQiOjEs#zc1MjY1NzZ9.yiONgsuT9bxgVml3Lxw4bS0Ho_qgLyYDKKVLzz9G4iI"

        with self.assertRaises(AuthenticationFailed):
            CustomUserAuthentication().authenticate(request)

    @freeze_time("2012-02-28")
    def test_authenticate_renew(self):
        request = HttpRequest()
        request.COOKIES[
            "jwt"
        ] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNjc3NjEyOTc2LCJpYXQiOjE2Nzc1MjY1NzZ9.yiONgsuT9bxgVml3Lxw4bS0Ho_qgLyYDKKVLzz9G4iI"

        with self.assertRaises(AuthenticationFailed):
            CustomUserAuthentication().authenticate(request)
