from django.db import models

# Create your models here.

class User(models.Model):
    models.EmailField(("unique=True"), max_length=254)
    models.CharField(max_length=254)
    
   

    def __str__(self):
        return self.email
    
class Category(models.Model):
    name = models.CharField(max_length=245)
    description = models.TextField(blank=True, null=True)
    def __str(self):
        return self.name
   
    
class Product(models.Model):
    CATEGORY_CHOICES =[
        ('new','New Arrivals'),
        ('popular','Popular'),
    ]    
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8,decimal_places=2)
    image = models.ImageField(upload_to='product/')
    Category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='product')
    tag = models.CharField(max_length=50,blank=True,null=True)
    is_discounted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=10, blank=True, null=True)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    