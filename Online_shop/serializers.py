from rest_framework import serializers

class PublicProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, read_only=True)
    sale_price = serializers.IntegerField(read_only=True)
    token = serializers.CharField(max_length=50, read_only=True)

class PublicCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class PublicCartSerializer(serializers.Serializer):
    product = PublicProductSerializer(read_only=True)
    quantity = serializers.IntegerField(read_only=True)

class PublicUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, read_only=True)
    email = serializers.CharField(max_length=100, read_only= True )

class PublicReviewSerializer(serializers.Serializer):
    user = PublicUserSerializer()
    review = serializers.CharField(max_length=100)
    star = serializers.IntegerField()