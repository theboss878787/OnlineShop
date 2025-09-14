from django.conf.urls.static import static
from django.urls import  path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, \
    PasswordChangeView, PasswordResetConfirmView

urlpatterns = [
    path('products/', views.Products.as_view(), name = 'products'),
    path('products/<str:token>/',views.ProductRetrieve.as_view(),name = 'product_detail' ),
    path('search/', views.SearchProduct.as_view(), name = 'search'),

    path('csrf/', views.csrf, name = 'csrf'),

    path('categories/', views.Categories.as_view(), name = "categories"),
    path('categories/<str:category>/', views.CategoryProducts.as_view(), name='category_products'),

    path('token/', views.ObtainAuthToken.as_view(), name = 'get_token'),
    path('register/', views.Register.as_view(), name = 'register'),

    path('order/', views.Order.as_view(), name = "order"),

    path('review/', views.ReviewCreate.as_view(), name = 'review'),

    path('cart/add/',views.CartCreate.as_view(), name = 'add_to_cart'),
    path('cart/decrease/', views.CartDecrease.as_view(), name = 'decrease_quantity'),
    path('cart/update/', views.UpdateQuantity.as_view(), name = 'update_quantity'),
    path('cart/clear/', views.ClearCart.as_view(), name='clear_cart'),
    path('cart/', views.CartList.as_view(), name = "cart_list"),

    path('profile/', views.ProfileView.as_view(), name = 'profile'),

    path('profile/addresses/', views.AddressList.as_view(), name = 'address_list'),

    path('login/', views.LoginView.as_view(), name = 'login'),
    path('logout/', views.LogoutView.as_view(), name= 'logout'),
    path('auth_me/', views.AuthMe.as_view(),name = 'auth'),
    path('auth/password_reset/', PasswordResetView.as_view(), name = "password_reset"),
    path('auth/password_reset_done/', PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('auth/password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view() ,name = 'password_reset_confirm'),
    path('auth/password_reset_complete/', PasswordResetCompleteView.as_view(), name = 'password_reset_complete')
]