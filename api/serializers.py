from rest_framework import serializers
#Models :
from .models import Product, Cart, Category, Order
#PublicSerilalizers :
from Online_shop.serializers import PublicCategorySerializer, PublicCartSerializer, PublicUserSerializer, PublicProductSerializer

class ProductSerializer(serializers.ModelSerializer):

    category = PublicCategorySerializer()
    class Meta:
        model = Product
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):

    product = PublicProductSerializer(read_only=True)

    def create(self, validated_data):
        cart = Cart.objects.filter(**validated_data, ordered = False).first()
        if cart:
            cart.quantity += 1
            cart.save()
            return cart
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

    def create(self, validated_data):
        user = validated_data.get('user')
        carts = Cart.objects.filter(user = user, ordered = False)
        if carts.first():
            order = Order.objects.create(**validated_data,price = 0)
            for cart in carts:
                order.cart.add(cart)
                cart_price = cart.product.price * cart.quantity
                cart.ordered = True
                order.price += cart_price
                cart.save()
                order.save()
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
                'cart',
                'date',

        ]
