from django.contrib.auth import get_user_model
from django.test import TestCase

from shop.models import Manufacturer, AutoPart


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test man",
            country="Test country"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_autopart_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test man",
            country="Test country"
        )

        autopart = AutoPart.objects.create(
            part_name="testname",
            price=25.5,
            manufacturer=manufacturer
        )

        self.assertEqual(
            str(autopart),
            f"{autopart.part_name}, price: ({autopart.price})"
        )

    def test_customer_str(self):
        customer = get_user_model().objects.create_user(
            username="testuser",
            password="testuser1232",
            first_name="test",
            last_name="user",
        )
        self.assertEqual(
            str(customer),
            f"{customer.username} ({customer.first_name} {customer.last_name})"
        )
