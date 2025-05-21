from rest_framework import serializers

class PublicProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    token = serializers.CharField(max_length=50)

class PublicCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class PublicCartSerializer(serializers.Serializer):
    product = PublicProductSerializer(read_only=True)
    quantity = serializers.IntegerField(read_only=True)

class PublicUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, read_only=True)
    email = serializers.CharField(max_length=100, read_only= True )