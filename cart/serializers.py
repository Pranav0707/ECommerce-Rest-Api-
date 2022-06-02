from rest_framework.serializers import ModelSerializer

from products.serializers import ProductSerializer

from .models import Cart, CartItem
from rest_framework import serializers

class CartSerializer(ModelSerializer):
    class Meta:
        model=Cart
        fields="__all__"

class CartItemSerializer(ModelSerializer):
    cart=CartSerializer()
    item=ProductSerializer()
    class Meta:
        model=CartItem
        fields="__all__"