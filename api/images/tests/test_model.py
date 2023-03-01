import os
from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from images.exceptions import ExpiredLinkException
from images.models import Image
from user.models import User


class ImageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.image = Image.objects.create(owner=self.user)

        path = os.path.join("images", "tests", "test_images", "test_image.png")
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} does not exist")
        with open(path, "rb") as f:
            image_data = f.read()
            image_file = SimpleUploadedFile(
                name="test_image.png", content=image_data, content_type="image/jpeg"
            )
        self.image.image = image_file
        self.image.save()

    def tearDown(self):
        os.remove(self.image.image.path)

    def test_resize(self):
        resized_image = self.image.resize(200)
        self.assertIsNotNone(resized_image)
        self.assertGreater(len(resized_image), 0)

    def test_validate_expiration_when_time_is_none(self):
        self.image.validate_expiration()

    def test_validate_expiration_when_time_is_in_future(self):
        self.image.expiration_time = timezone.now() + timedelta(days=1)
        self.image.validate_expiration()

    def test_validate_expiration_when_time_is_in_past(self):
        self.image.expiration_time = timezone.now() - timedelta(days=1)
        with self.assertRaises(ExpiredLinkException):
            self.image.validate_expiration()

    def test_str(self):
        expected = self.image.image.name
        self.assertIn(str(self.image), expected)

    def test_extension(self):
        self.assertEqual(self.image.extension(), "png")
