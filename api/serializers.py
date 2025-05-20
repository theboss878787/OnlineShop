from rest_framework import serializers
#Models :
from .models import Product, Cart, Category

from Online_shop.serializers import PublicCategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category = PublicCategorySerializer()
    class Meta:
        model = Product
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        cart = Cart.objects.filter(**validated_data, ordered = False).first()
        if cart:
            cart.quantity += 1
            cart.save()
            return cart
        cart = Cart.objects.create(**validated_data)
        return cart

    class Meta:
        model = Cart
        fields =[
            'product',
            'quantity',
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]