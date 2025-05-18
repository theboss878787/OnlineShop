from django.conf.urls.static import static
from django.urls import  path
from . import views
urlpatterns = [
    path('products/', views.products, name = 'products'),
    path('products/<str:token>/',views.ProductRetrieve.as_view(),name = 'product_detail' ),
    path('categories/<str:category>/', views.CategoryProducts.as_view(), name='category_products'),

]