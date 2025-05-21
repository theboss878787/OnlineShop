from django.conf.urls.static import static
from django.urls import  path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('products/', views.products, name = 'products'),
    path('products/<str:token>/',views.ProductRetrieve.as_view(),name = 'product_detail' ),

    path('categories/', views.Categories.as_view(), name = "categories"),
    path('categories/<str:category>/', views.CategoryProducts.as_view(), name='category_products'),

    path('order/', views.Order.as_view(), name = "order"),
    path('token/', obtain_auth_token, name = 'get_token'),
    path('add_to_cart/',views.CartCreate.as_view(), name = 'add to cart')
]