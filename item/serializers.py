from dataclasses import fields
from rest_framework import serializers
from item.models import Category, Item, Order, ItemOrder

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["__all__"]


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class ItemOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = ItemOrder
        fields = "__all__"
