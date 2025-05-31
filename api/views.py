from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
#Models :
from .models import Product, Category, Cart, Order, ProductReview
from django.contrib.auth.models import User
#Seializers :
from .serializers import ProductSerializer, CartSerializer, CategorySerializer, OrderSerializer, UserSerializer, ReviewSerializer

from rest_framework.response import Response
from rest_framework import generics

@api_view(['GET'])
def products(request):

    product = Product.objects.all()
    serializer = ProductSerializer(product, many = True)
    return  Response(serializer.data)

class Register(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

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
class  CartList(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication
    ]
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user = self.request.user, ordered = False)
        return qs
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
        serializer.save(user =user, product=product)

class Order(generics.ListCreateAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication
    ]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = user)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        qs = qs.filter(user = user)
        return qs

class ReviewCreate(generics.CreateAPIView):
    queryset = ProductReview.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        product_token = self.request.data.get('product_token')
        print(product_token)
        product = Product.objects.filter(token = product_token).first()
        user = self.request.user
        serializer.save(user = user, product= product)