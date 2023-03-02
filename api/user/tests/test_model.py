from django.test import TestCase
from rest_framework.exceptions import PermissionDenied

from user.models import Size, Tier, User


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

        self.user_basic = self.create_user("admin", self.tier_basic)
        self.user_premium = self.create_user("adminPro", self.tier_permium)

    def create_user(self, username, tier):
        user = User.objects.create(
            username=username,
            password="qwerty",
            image_tier=tier,
        )
        return user

    def test_validator_tiers(self):
        self.user_basic.validator_tiers(200)
        self.user_basic.validator_tiers(400)
        self.user_basic.validator_tiers("200")
        self.user_basic.validator_tiers("400")

    def test_validator_tiers_bad_size(self):
        with self.assertRaises(PermissionDenied):
            self.user_basic.validator_tiers(600)

        with self.assertRaises(PermissionDenied):
            self.user_basic.validator_tiers("600")

        with self.assertRaises(PermissionDenied):
            self.user_basic.validator_tiers("original")

    def test_validator_tiers_original(self):
        self.user_premium.validator_tiers("original")
