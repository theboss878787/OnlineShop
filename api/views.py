from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product,Category
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import generics

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@api_view(['GET'])
def products(request):

    product = Product.objects.all()
    serializer = ProductSerializer(product, many = True)
    return  Response(serializer.data)

class ProductRetrieve(generics.RetrieveAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field  = 'token'
class CategoryProducts(generics.ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category_name = self.kwargs.get('category')
        category = Category.objects.filter(name__iexact = category_name).first()

        return qs.filter(category = category)
