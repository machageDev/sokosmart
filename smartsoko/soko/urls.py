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
    path('contact',views.contact,name='contact')
    
]
