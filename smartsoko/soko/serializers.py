from rest_framework import serializers
from .models import User,Category,CartItem,Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name','email')

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','description')
        
class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','description','price','category','tag','is_discounted','created_at')
        
class CartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields =  ['id', 'product', 'quantity', 'color', 'size', 'total_price']
        
def get_total_price(self, obj):
        return obj.total_price()        