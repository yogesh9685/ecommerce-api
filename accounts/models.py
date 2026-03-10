from django.db import models
from django.contrib.auth.models import User, AbstractUser

class CustomUser(AbstractUser):
     
    email = models.EmailField(blank = False , unique = True)
    is_verified = models.BooleanField(default=False)
    is_seller = models.BooleanField(default = False)
    ROLE_CHOICES = (

        ("customer","Customer"),
        ("seller","Seller")

    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
 

class OTPVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):

    name = models.CharField(max_length=200)

    image = models.ImageField(upload_to="categories/")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=255)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField()

    category = models.ForeignKey(Category , on_delete=models.CASCADE,  related_name="products")

   
    seller = models.ForeignKey(CustomUser , on_delete=models.CASCADE, related_name="products")
    
    image = models.ImageField(upload_to="products/")
        
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




from django.db import models
from django.conf import settings


class Cart(models.Model):

    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)

    
    quantity = models.PositiveIntegerField(default=1)


    created_at = models.DateTimeField(auto_now_add=True)