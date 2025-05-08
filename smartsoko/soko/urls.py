from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('dashboard',views.dashboard,name='dashboard'),
    
    path('product',views.product,name='product'),
    path('product_detail',views.product_detail,name='product_detail'),
    path('about',views.about, name='about'),
    path('faqs',views.FAQS, name='FAQS'),
    path('contact',views.contact,name='contact'),
    path('cart', views.cart, name='cart'),
    
    
    #api URLS
    path('apiregister',views.apiregister,name='apiregister'),
    path('apilogin',views.apilogin,name='api_login'),
    path('api/product/<int:pk>', views.apiproduct_detail, name='product-detail'),
    path('api/product/related', views.apirelated_products, name='related-products'),
    path('api/cart/add', views.apiadd_to_cart, name='add-to-cart')
    
]
