from rest_framework import serializers


class PublicCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
