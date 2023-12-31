from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class MyUser(AbstractUser):
    user_id = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)


class Product(models.Model):
    product_id = models.CharField(max_length=250, blank=True)
    name = models.CharField(max_length=250)
    description = models.TextField(default="Product Description")
    sub_description = models.CharField(max_length=100, default="Product Description")
    price = models.CharField(max_length=10)
    image_url = models.CharField(max_length=500)
    image_url_3d = models.CharField(max_length=500)
    color = models.CharField(max_length=20, blank=True)
    badge = models.CharField(max_length=20, blank=True, null=True)


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='cartitems')
    itemname = models.CharField(max_length=250)
    itemprice = models.CharField(max_length=10)
    itemquantity = models.CharField(max_length=3)

class Order(models.Model):
    order_id = models.CharField(max_length=250, blank=True)
    user_id = models.CharField(max_length=250)
    cart_id = models.CharField(max_length=250)
    created_at = models.CharField(max_length=16)
