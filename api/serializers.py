from unicodedata import category

from rest_framework import serializers
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
#Models :
from .models import Product, Cart, Category, Order, ProductReview
from django.contrib.auth.models import User
#PublicSerilalizers :
from Online_shop.serializers import PublicCategorySerializer, PublicCartSerializer, PublicUserSerializer, PublicProductSerializer, PublicReviewSerializer

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

    def create(self, validated_data):

        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email'
        ]

class CartSerializer(serializers.ModelSerializer):

    product = PublicProductSerializer(read_only=True)

    def create(self, validated_data):
        cart = Cart.objects.filter(**validated_data, ordered = False).first()
        product = validated_data.get('product')
        if cart:
            if cart.quantity >= product.in_stock:
                raise serializers.ValidationError({'Message ' : f"{cart.product.name} is out of stock"})
            cart.quantity += 1
            cart.save()
            return cart
        if product.in_stock <= 0 :
            raise serializers.ValidationError({'Message ': f"{product.name} is out of stock"})

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

class OrderSerializer(serializers.ModelSerializer):

    cart = serializers.SerializerMethodField()
    date = serializers.DateTimeField(read_only=True)
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
                'cart',
                'date',

        ]

class ReviewSerializer(serializers.ModelSerializer):

    user = PublicUserSerializer(read_only=True)
    product = PublicProductSerializer(read_only=True)
    class Meta:
        model = ProductReview
        fields = [
            'user',
            'product',
            'review',
            'star',
        ]
