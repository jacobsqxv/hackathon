from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class MyUser(AbstractUser):
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image_url = models.CharField(max_length=250)


class Cart(models.Model):
    product_id = models.CharField(max_length=250)


class Order(models.Model):
    user_id = models.CharField(max_length=250)
    product_id = models.CharField(max_length=250)
