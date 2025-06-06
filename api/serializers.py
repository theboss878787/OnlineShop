from rest_framework.response import Response
from rest_framework import serializers
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from drf_yasg.utils import swagger_serializer_method
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

#Models :
from .models import Product, Cart, Category, Order, ProductReview
from django.contrib.auth.models import User
#PublicSerilalizers :
from Online_shop.serializers import PublicTokenSerializer,PublicCategorySerializer, PublicCartSerializer, PublicUserSerializer, PublicProductSerializer, PublicReviewSerializer

def send_order_email(to_email, items, price, token):
    subject ="سفارش شما تایید شد"

    html_content = render_to_string("emails/order_confirmation.html", {
        "items": items,
        "total_price": price,
        "token": token,
    })

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
         [to_email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

class ProductSerializer(serializers.ModelSerializer):

    category = PublicCategorySerializer()
    reviews = serializers.SerializerMethodField(read_only=True)
    sale_price = serializers.FloatField(read_only=True)

    @swagger_serializer_method(serializer_or_field=PublicReviewSerializer(many=True))
    def get_reviews(self, obj):
        reviews = obj.reviews
        return PublicReviewSerializer(reviews, many=True).data
    class Meta:
        model = Product
        fields = [
            'token',
            'name',
            'price',
            'discount',
            'sale_price',
            'in_stock',
            'category',
            'description',
            'image',
            'extra_details',
            'reviews'
        ]

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    @swagger_serializer_method(serializer_or_field=PublicTokenSerializer())
    def get_token(self, obj):
        token = Token.objects.create(user = obj)
        return PublicTokenSerializer(token).data
    def create(self, validated_data):

        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    class Meta:
        model = User
        fields = [
            'token',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',

        ]

class CartCreateSerializer(serializers.ModelSerializer):

    product_token = serializers.CharField(max_length=100, write_only=True)

    def create(self, validated_data):
        token = validated_data.pop('product_token')
        try:
            product = Product.objects.get(token=token)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product_token': 'Invalid token'})
        cart = Cart.objects.filter(**validated_data, ordered = False, product = product).first()

        if cart:
            if cart.quantity >= product.in_stock:
                raise serializers.ValidationError({'Message ' : f"{cart.product.name} is out of stock"})
            cart.quantity += 1
            cart.save()
            return cart
        if product.in_stock <= 0 :
            raise serializers.ValidationError({'Message ': f"{product.name} is out of stock"})

        cart = Cart.objects.create(**validated_data,product=product)
        return cart

    class Meta:
        model = Cart
        fields =[
            'product_token',
            'quantity',

        ]
class CartInputSerializer(serializers.Serializer):
    product_token = serializers.CharField()

class CartListSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = [
            'product',
            'quantity',
        ]
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]

class OrderSerializer(serializers.ModelSerializer):

    cart = serializers.SerializerMethodField()
    date = serializers.DateTimeField(required=False)
    user = PublicUserSerializer(read_only = True)
    price = serializers.IntegerField(read_only=True)
    status = serializers.CharField(max_length=50,read_only=True)

    def create(self, validated_data):
        user = validated_data.get('user')
        carts = Cart.objects.filter(user = user, ordered = False)
        if carts.first():
            for cart in carts:
                product = cart.product
                if cart.quantity > product.in_stock :
                    raise serializers.ValidationError({"Message": "Some products are out of stock"})

            order = Order.objects.create(**validated_data,price = 0)

            for cart in carts:
                product = cart.product
                product.in_stock -= cart.quantity
                product.save()

                order.cart.add(cart)
                cart_price = cart.product.sale_price * cart.quantity
                order.price += cart_price
                cart.ordered = True

                cart.save()
                order.save()

                send_order_email(items = carts, price=order.price, to_email=user.email, token=order.token[2:])
            return order
        raise serializers.ValidationError({"Message" : "Cart is empty"})

    def get_cart(self,obj):
        carts = obj.cart.all()
        return PublicCartSerializer(carts, many=True).data

    class Meta:
        model = Order
        fields = [
                'user',
                'address',
                'number',
                'city',
                'price',
                'status',
                'postal_code',
                'cart',
                'date',

        ]

class ReviewSerializer(serializers.ModelSerializer):

    product_token = serializers.CharField(max_length=100, write_only=True)
    def create(self,validated_data):

        token = validated_data.pop('product_token')
        try:
            product = Product.objects.get(token=token)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product_token': 'Invalid token'})

        return ProductReview.objects.create(product=product, **validated_data)

    class Meta:
        model = ProductReview
        fields = [
            'review',
            'star',
            'product_token'
        ]

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    @swagger_serializer_method(serializer_or_field=PublicUserSerializer())
    def get_user(self, obj):
        return PublicUserSerializer(obj['user']).data
