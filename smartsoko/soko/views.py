from django.shortcuts import render
from urllib import request
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect 
from soko.models import Product, User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


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

def FAQS(request):
    return render(request, FAQS.html)   

def home(request):
    return render(request,'home.html')      



def contact(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Basic validation
        if not all([name, email, message]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'contact.html')

        # Send email (configure your email settings in settings.py)
        try:
            send_mail(
                subject=f"New Contact Form Submission from {name}",
                message=f"""
                Name: {name}
                Email: {email}
                Phone: {phone}
                
                Message:
                {message}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')  # Redirect to clear the form
        
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again later.')
            print(f"Error sending email: {e}")  # For debugging

    return render(request, 'contact.html')  