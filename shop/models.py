from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


class AutoPart(models.Model):
    part_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    manufacturer = models.ForeignKey(
        to=Manufacturer,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = "auto_parts"

    def __str__(self):
        return f"{self.part_name}, price: ({self.price})"


class Customer(AbstractUser):

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Order(models.Model):
    auto_parts = models.ManyToManyField(to=AutoPart, related_name="orders")
    customers = models.ManyToManyField(to=Customer, related_name="orders")

    def __str__(self):
        return f"Order number: {self.id}"
