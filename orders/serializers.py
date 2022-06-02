
from rest_framework import serializers

from .models import Address, Order,OrderItem

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields="__all__"