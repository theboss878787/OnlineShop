from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.generics import ListAPIView
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView

from Online_shop.serializers import PublicUserSerializer
#Models :
from .models import Product, Category, Cart, Order, ProductReview, Profile, Address
from django.contrib.auth.models import User
#Seializers :
from .serializers import ProductSerializer, CartCreateSerializer, CategorySerializer, OrderSerializer, UserSerializer, \
    ReviewSerializer, PublicCartSerializer, AuthTokenSerializer, TokenResponseSerializer, CartListSerializer, \
    CartInputSerializer, OrderInputSerializer, ProfileSerializer, AddressSerializer

from rest_framework.response import Response
from rest_framework import generics, permissions, status


def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

class Products(generics.ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SearchProduct(generics.ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        q = self.request.GET.get('q')
        qs = super().get_queryset()
        qs = qs.filter(Q(name__icontains = q)| Q (description__icontains = q))
        return qs
class AuthMe(APIView):
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        user = request.user
        return Response(UserSerializer(user).data)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Logged in successfully"})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})
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
class CartList(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartListSerializer

    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user = self.request.user, ordered = False)
        return qs
class CartCreate(generics.CreateAPIView):

    queryset = Cart.objects.all()
    serializer_class = CartCreateSerializer

    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=CartInputSerializer,
        responses={
            200: CartListSerializer,
            400: "Send the product token",
            404: "Product not found",
            401: ""
        }
    )
    def post(self, request):
        return super().post(request)

    def perform_create(self,serializer):

        user = self.request.user
        serializer.save(user =user)

class CartDecrease(APIView):

    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        request_body=CartInputSerializer,
        responses={
            200: CartListSerializer,
            400: "Send the product token",
            404: "Product not found",
            401: ""
        }
    )

    def put(self,request):
        user = request.user
        product_token = request.data.get('product_token')
        if not product_token:
            return Response({'error': 'Send the product token.'}, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.filter(token = product_token).first()
        if not product:
            return Response({'error': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)

        cart = Cart.objects.filter(user = user, product=product, ordered = False).first()
        if not cart :
            return Response({'error': 'This Product is not in your cart.'}, status=status.HTTP_400_BAD_REQUEST)
        if cart.quantity >1 :
            cart.quantity -= 1
            cart.save()
            return Response(CartListSerializer(cart).data, status=status.HTTP_200_OK)
        else:
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
class ClearCart(APIView):

    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        carts = Cart.objects.filter(user=user, ordered = False)
        if carts:
            for cart in carts:
                cart.delete()
            return Response({'detail': 'Done!'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Cart is empty!'}, status=status.HTTP_204_NO_CONTENT)

class UpdateQuantity(APIView):

    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=CartInputSerializer,
        responses={
            200: CartListSerializer,
            400: "Send the product token",
            404: "Product not found",
            401: ""
        }
    )

    def put(self,request):
        serializer = CartListSerializer
        user = request.user

        product_token = request.data.get('product_token')
        if not product_token:
            return Response({'error': 'Send the product token.'}, status=status.HTTP_400_BAD_REQUEST)

        quantity = request.data.get('quantity')
        if not quantity:
            return Response({'error': 'Send the quantity.'}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.filter(token = product_token).first()
        if not product:
            return Response({'error': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)
        if quantity>product.in_stock :
            return Response({'error': f'{product.name} Is out of stock.'}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.filter(user = user, product=product, ordered = False).first()
        if not cart:
            cart = Cart.objects.create(product= product, user = user, quantity=quantity, ordered = False)
            return Response(serializer(cart).data)

        cart.quantity = quantity
        cart.save()
        return Response(serializer(cart).data)


class Order(generics.ListCreateAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        user = self.request.user
        serializer.save(user = user, first_name= first_name, last_name= last_name)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        qs = qs.filter(user = user)
        return qs
    @swagger_auto_schema(
        request_body=OrderInputSerializer,
        operation_description = 'For existing address don`t send city,address_text,postal_code just send address_id.',
        responses= {
            201: OrderSerializer
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request)

class AddressList(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = user, save_address=True)


class ReviewCreate(generics.CreateAPIView):
    queryset = ProductReview.objects.all()
    serializer_class = ReviewSerializer

    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = user)

class ProfileView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]


class ObtainAuthToken(APIView):

    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    @swagger_auto_schema(
        request_body=AuthTokenSerializer,
        responses={200: TokenResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response(TokenResponseSerializer({'token': token, 'user' : user}).data)


