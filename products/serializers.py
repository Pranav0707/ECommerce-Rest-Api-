import imp
from attr import fields
from rest_framework import serializers
from .models import Product,Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=["id","name","slug","products"]

class ProductSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    class Meta:
        model=Product
        fields="__all__"

class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"

class CreateProductSerializer(serializers.ModelSerializer):
    # products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model=Product
        fields=["name","description","price","category","items_in_stock","slug"]
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['category']=CategorySerializer(instance.category).data
        return response