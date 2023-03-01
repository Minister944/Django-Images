from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from user.models import User, Tier, Size
from images.models import Image
from images.serializer import ImageSerializer
from rest_framework.test import force_authenticate
import os
from django.core.files.uploadedfile import SimpleUploadedFile


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

        self.user = User.objects.create(
            username="testuser",
            password="testpass",
            image_tier=self.tier_basic,
        )

        self.user_premium = User.objects.create(
            username="testuserpremium",
            password="testpass",
            image_tier=self.tier_permium,
        )

    def test_upload_image(self):
        self.client.force_authenticate(user=self.user)

        image_path = "images/tests/test_images/test_image.png"
        with open(image_path, "rb") as f:
            image_data = f.read()
        image_file = SimpleUploadedFile(
            "test_image.png", image_data, content_type="image/png"
        )

        response = self.client.post(reverse("upload-image"), {"image": image_file})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        image = Image.objects.get(id=response.data["id"])
        self.assertTrue(image.owner == self.user)
        self.assertTrue(image.expiration_time is None)

    def test_thumbnail_generation(self):
        self.client.force_authenticate(user=self.user)

        image_path = "images/tests/test_images/test_image.png"
        with open(image_path, "rb") as f:
            image_data = f.read()
        image_file = SimpleUploadedFile(
            "test_image.png", image_data, content_type="image/png"
        )

        response = self.client.post(reverse("upload-image"), {"image": image_file})

        thumbnail_links = response.data["thumbnails"]
        self.assertTrue(len(thumbnail_links) == 2)
        self.assertIn("400px", thumbnail_links)
        self.assertIn("200px", thumbnail_links)

        response = self.client.get(thumbnail_links["200px"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission(self):
        self.client.force_authenticate(user=self.user)

        image_path = "images/tests/test_images/test_image.png"
        with open(image_path, "rb") as f:
            image_data = f.read()
        image_file = SimpleUploadedFile(
            "test_image.png", image_data, content_type="image/png"
        )

        response = self.client.post(reverse("upload-image"), {"image": image_file})

        thumbnail_links = response.data["thumbnails"]

        response = self.client.get("http://testserver/api/image/999/200")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(user=self.user_premium)
        response = self.client.get(thumbnail_links["200px"])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
