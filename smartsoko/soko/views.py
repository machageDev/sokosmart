from django.shortcuts import render
from urllib import request
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect 
from soko.models import Product, User


# Create your views here.
def login(request):
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect(dashboard)
        else:
            return render(request,"login.html",{"error":"invalid credentials"})
    return render(request,'login.html')
            
def register(request):
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get(password)
        if User.objects.filter(email=email).exist():
            return render(request,"register.html", {"Error:" "Email already exist"})
        User.objects.create_user(email=email,password=password)
        return redirect(login)
    return render(request,"register.html")

def dashboard(request):
     return render(request,dashboard.html)
        
from django.shortcuts import render, get_object_or_404
from .models import Product

def product(request):
    new_arrivals = Product.objects.filter(category__name='New Arrivals')
    popular_products = Product.objects.filter(category__name='Popular')

    context = {
        'new_arrivals': new_arrivals,
        'popular_products': popular_products,
    }
    return render(request, 'products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

def about(request):
    return render(request,'about.html')

              