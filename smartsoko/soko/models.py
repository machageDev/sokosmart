from django.db import models

# Create your models here.

class User(models.Model):
    models.EmailField(("unique=True"), max_length=254)
    models.CharField(max_length=254)
    
   

    def __str__(self):
        return self.email
    