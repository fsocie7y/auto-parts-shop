from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from shop.models import Manufacturer

MANUFACTURER_URL = reverse("shop:manufacturer-list")


class ManufacturerViewTests(TestCase):
    def setUp(self) -> None:
        self.manuf = get_user_model().objects.create_user(
            username="testuser",
            password="test123user"
        )
        self.client.force_login(self.manuf)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Manuf12",
            country="testcountry1"
        )
        Manufacturer.objects.create(
            name="Manuf34",
            country="testcountry2"
        )

        manufs = Manufacturer.objects.all()

        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufs)
        )
        self.assertTemplateUsed(response, "shop/manufacturer_list.html")
