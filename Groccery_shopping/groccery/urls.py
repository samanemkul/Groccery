from django.contrib import admin
from django.urls import path,include
from groccery import views

urlpatterns = [
    path("", views.home, name='home'),
    path("signup",views.signup.as_view(), name='signup'),
    path("login",views.login.as_view(), name='login'),
    path("productdetail/<int:pk>",views.productdetail,name="productdetail"),
    path("logout",views.logout, name='logout'),
    path("add_to_cart",views.add_to_cart, name='add_to_cart'),
    path("showcart",views.showcart, name='showcart'),
    path("plus_cart", views.plus_cart, name='plus_cart'),
    path("minus_cart", views.minus_cart, name='minus_cart'),
    path("remove_cart", views.remove_cart, name='remove_cart'),
    path("checkout", views.checkout, name='checkout'),
    path("process_checkout", views.process_checkout, name='process_checkout'),
    path('invoice/<int:order_id>/', views.invoice, name='invoice'),
    path("search",views.search,name='search')
]