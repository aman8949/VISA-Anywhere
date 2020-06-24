from django.urls import path
from . import views

app_name='shop'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('contact/', views.contact, name = "ShopContact"),
    path('products/<int:id>', views.productView, name='ProductView'),
    path('checkout/', views.checkout, name="Checkout"),
    path('login/', views.login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('register/', views.register, name='register'),
    path('merchant_list/', views.merchant_list, name='merchant_list'),
    path('product_list/<int:merchant_id>', views.product_list, name='product_list'),
]