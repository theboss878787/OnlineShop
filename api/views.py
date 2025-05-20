from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
#Models :
from .models import Product, Category, Cart
#Seializers :
from .serializers import ProductSerializer, CartSerializer, CategorySerializer

from rest_framework.response import Response
from rest_framework import generics

@api_view(['GET'])
def products(request):

    product = Product.objects.all()
    serializer = ProductSerializer(product, many = True)
    return  Response(serializer.data)
class Categories(generics.ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
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

class CartCreate(generics.CreateAPIView):

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication
    ]

    def perform_create(self,serializer):
        product_token = self.request.data.get('product_token')
        product = Product.objects.filter(token = product_token).first()
        user = self.request.user
        serializer.save(user =user,product=product)

