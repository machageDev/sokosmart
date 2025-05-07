from django.shortcuts import render
from urllib import request
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect 
from smartsoko.soko.serializers import UserSerializer
from soko.models import Product, User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import ValidationError

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
        

@login_required
def product(request):
    new_arrivals = Product.objects.filter(Category__name='New Arrivals')
    popular_products = Product.objects.filter(Category__name='Popular')

    context = {
        'new_arrivals': new_arrivals,
        'popular_products': popular_products,
    }
    return render(request, 'products.html', context)

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

def about(request):
    return render(request,'about.html')

def FAQS(request):
    return render(request, 'FAQS.html')   

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

@login_required
def cart(request):
    """Display the shopping cart"""
    cart = request.session.get('cart', {})
    
    # Prepare cart items with product details and totals
    cart_items = []
    total_price = 0
    total_items = 0
    
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * item['quantity']
        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'total': item_total
        })
        total_price += item_total
        total_items += item['quantity']
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_id):
    """Add a product to the cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    # Get quantity from POST data (default to 1 if not provided)
    quantity = int(request.POST.get('quantity', 1))
    
    if product_id in cart:
        # Update existing item
        cart[product_id]['quantity'] += quantity
    else:
        # Add new item
        cart[product_id] = {
            'quantity': quantity,
            'price': str(product.price)  # Store as string to avoid JSON serialization issues
        }
    
    request.session['cart'] = cart
    messages.success(request, f"{product.name} added to your cart")
    return redirect('cart:cart_view')

def remove_from_cart(request, product_id):
    """Remove a product from the cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        messages.success(request, f"{product.name} removed from your cart")
    
    return redirect('cart:cart_view')

def update_cart(request, product_id):
    """Update product quantity in the cart"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart[product_id]['quantity'] = quantity
            request.session['cart'] = cart
            messages.success(request, f"{product.name} quantity updated")
        else:
            # If quantity is 0 or less, remove the item
            return remove_from_cart(request, product_id)
    
    return redirect('cart:cart_view')


#api section by only and one giant MACHAGE
@api_view(['POST'])
@permission_classes([AllowAny])
def apiregister(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not email or not password:
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already in use.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_password(password)
    except ValidationError as e:
        return Response({'error': list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def apilogin(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(username=user.username, password=password)

    if user is not None:
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    