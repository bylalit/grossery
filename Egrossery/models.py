from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    image1 =  models.ImageField(upload_to='product_image')
    image2 =  models.ImageField(upload_to='product_image')
    image3 =  models.ImageField(upload_to='product_image')
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    price = models.FloatField()
    
    def __str__(self):
        return self.name
    
  
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    date = models.DateField(auto_now_add=True)
    total_amount = models.FloatField()
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

