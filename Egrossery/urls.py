from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('singal_product/<int:product_id>/', views.singal_page, name='singal_product'),
    path('product/<str:category_name>/', views.product, name='product'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path('update_cart/<int:product_id>/<str:action>/', views.update_cart, name="update_cart"),
    path('delete_cart/<int:product_id>/', views.delete_cart, name='delete_cart'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('add_address/', views.add_address, name='add_address'),
    path('place_order/', views.place_order, name='place_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    
    
    # Admin Urls
    path('admin_dash/', views.admin_dash, name='admin_dash'),
    path('product_list/', views.product_list, name='product_list'),
    path('order_list/', views.order_list, name='order_list'),
    path('login_dash/', views.login_dash, name='login_dash'),
    path('logout_dash/', views.logout_dash, name='logout_dash'),
    
]
