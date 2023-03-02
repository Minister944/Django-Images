import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from images.models import Image
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from user.models import Size, Tier, User


class ImageUploadViewIntegrationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.size200 = Size.objects.create(size=200)
        self.size400 = Size.objects.create(size=400)

        self.tier_basic = Tier.objects.create(name="Basic")
        self.tier_basic.thumbnail_sizes.add(self.size200)
        self.tier_basic.thumbnail_sizes.add(self.size400)

        self.tier_permium = Tier.objects.create(name="Premium", has_original=True)
        self.tier_permium.thumbnail_sizes.add(self.size200)
        self.tier_permium.thumbnail_sizes.add(self.size400)

        self.user_basic = self.create_user("admin", self.tier_basic)
        self.user_premium = self.create_user("adminPro", self.tier_permium)

        self.image_file = self.create_image_file()

    def create_user(self, username, tier):
        user = User.objects.create(
            username=username,
            password="qwerty",
            image_tier=tier,
        )
        return user

    def create_image_file(self):
        path = "images/tests/test_images/test_image.png"
        with open(path, "rb") as f:
            image_data = f.read()
        image_file = SimpleUploadedFile(
            "test_image.png", image_data, content_type="image/png"
        )
        return image_file

    def test_upload_image(self):
        self.client.force_authenticate(user=self.user_basic)

        response = self.client.post(reverse("upload-image"), {"image": self.image_file})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        image = Image.objects.get(id=response.data["id"])
        self.assertTrue(image.owner == self.user_basic)
        self.assertTrue(image.expiration_time is None)

    def test_thumbnail_generation(self):
        self.client.force_authenticate(user=self.user_basic)

        response = self.client.post(reverse("upload-image"), {"image": self.image_file})
        thumbnail_links = response.data["thumbnails"]
        self.assertTrue(len(thumbnail_links) == 2)
        self.assertIn("400px", thumbnail_links)
        self.assertIn("200px", thumbnail_links)

        response = self.client.get(thumbnail_links["200px"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission(self):
        self.client.force_authenticate(user=self.user_basic)

        response = self.client.post(reverse("upload-image"), {"image": self.image_file})
        thumbnail_links = response.data["thumbnails"]

        response = self.client.get("http://testserver/api/image/999/200")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(user=self.user_premium)
        response = self.client.get(thumbnail_links["200px"])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
