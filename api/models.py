from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import string ,random
from django.core.validators import MaxValueValidator, MinValueValidator
from django_jalali.db import models as jmodels
import jdatetime

def code_generator(type = 'P' , length = 7):  # Default for products
        code = type + '-'+''.join(random.choices(string.digits, k = length))
        return code

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(default='images/no_image.jpg')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.BigIntegerField()
    in_stock = models.PositiveIntegerField()
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    extra_details = models.TextField(null=True, blank=True, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    token= models.CharField(blank= True, max_length=10,null= True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = code_generator()
        super().save(*args, **kwargs)
    @property
    def sale_price(self):
        return int(self.price - self.price * (self.discount/100))

    def __str__(self):
        return '{} - {}'.format(self.name, self.category)
class ProductReview(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    star_choices = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    ]
    star = models.IntegerField(choices=star_choices)

    def __str__(self):
        return f'{self.user} - {self.star} Stars'

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return (f"{self.quantity} of {self.product.name} for {self.user.username} ")

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=12)
    save_address = models.BooleanField(default=False)

class Order(models.Model):
    status_choices = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('OnTheWay', 'OnTheWay'),
        ('Canceled', 'Canceled'),
        ('Completed', 'Completed')
    )
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    cart = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=11)
    price = models.BigIntegerField()
    date = jmodels.jDateTimeField(default=jdatetime.datetime.now)
    token= models.CharField(blank= True,max_length=10,unique =True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = code_generator('O' , 7)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order of {self.user} is {self.status}. Date : {self.date.ctime()}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    addresses = models.ManyToManyField(Address)
    phone_number = models.CharField(max_length=11, unique=True, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}`s Profile'
