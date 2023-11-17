from rest_framework import serializers
from base.models import Product, Order, Cart, CartItem
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        skip_fields = ["product_id"]

        def to_representation(self, instance):
            data = super().to_representation(instance)
            for field in self.skip_fields:
                data.pop(field, None)

            return data


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        skip_fields = ["cart_id"]

        def to_representation(self, instance):
            data = super().to_representation(instance)
            for field in self.skip_fields:
                data.pop(field, None)

            return data


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["itemname", "itemprice", "itemquantity", "product_id"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        skip_fields = ["order_id"]

        def to_representation(self, instance):
            data = super().to_representation(instance)
            for field in self.skip_fields:
                data.pop(field, None)

            return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
        )

        return user
