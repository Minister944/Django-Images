from django.test import TestCase

from user.models import User, Tier, Size

from rest_framework.exceptions import PermissionDenied


class UserTestCase(TestCase):
    def setUp(self):
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

    def test_validator_tiers(self):
        self.user.validator_tiers(200)
        self.user.validator_tiers(400)
        self.user.validator_tiers("200")
        self.user.validator_tiers("400")

    def test_validator_tiers_bad_size(self):
        with self.assertRaises(PermissionDenied):
            self.user.validator_tiers(600)

        with self.assertRaises(PermissionDenied):
            self.user.validator_tiers("600")

        with self.assertRaises(PermissionDenied):
            self.user.validator_tiers("original")

    def test_validator_tiers_original(self):
        self.user_premium.validator_tiers("original")
