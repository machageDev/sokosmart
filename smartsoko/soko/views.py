from django.shortcuts import render
from urllib import request
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect 
from soko.models import User


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
        
                