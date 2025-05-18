from rest_framework import serializers
from .models import Product
from Online_shop.serializers import PublicCategorySerializer
class ProductSerializer(serializers.ModelSerializer):
    category = PublicCategorySerializer()
    class Meta:

        model = Product
        fields = "__all__"

