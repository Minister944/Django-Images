from django.test import TestCase
from images.models import Image
from images.serializer import ImageSerializer
from user.models import User


class ImageSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

        self.serializer_images = {
            "owner": self.user,
        }

        self.image = Image.objects.create(**self.serializer_images)
        self.serializer = ImageSerializer(instance=self.image)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["image", "expiration_time"]))

    def test_expiration_time_is_none(self):
        data = self.serializer.data
        self.assertIsNone(data["expiration_time"])
