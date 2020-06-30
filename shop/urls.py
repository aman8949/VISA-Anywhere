from django.urls import path
from . import views

app_name='shop'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('contact/', views.contact, name = "ShopContact"),
    # path('products/<int:id>', views.productView, name='ProductView'),
    path('checkout/<int:merchant_id>', views.checkout, name="checkout"),
    path('login/', views.login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('register/', views.register, name='register'),
    path('merchant_list/search/',views.search , name='search'),
    path('merchant_list/', views.merchant_list, name='merchant_list'),
    path('merchant_list2/', views.merchant_list2, name='merchant_list2'),
    path('product_list/<int:merchant_id>', views.product_list, name='product_list'),
    path('merchant_homepage', views.merchant_homepage, name='merchant_homepage'),
    path('product_delete/<int:product_id>', views.product_delete, name='product_delete'),
    path('product_add/',views.product_add, name='product_add'),
    path('mer_order_list/',views.mer_order_list, name='mer_order_list'),
    path('mer_order_detail/<int:order_id>', views.mer_order_detail, name='mer_order_detail'),
    path('user_order_list/',views.user_order_list, name='user_order_list'),
    path('user_order_detail/<int:order_id>', views.user_order_detail, name='user_order_detail'),
    path('load_json/',views.load_json, name='load_json'),
    path('load_queue_json/',views.load_queue_json, name='load_queue_json'),
]