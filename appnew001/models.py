from django.db import models
from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Login(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=128)  # added max_length

    def __str__(self):
        return self.email   


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # renamed from username → user
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
    












class user(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField()
    phone = models.IntegerField()
    address_line1 = models.CharField()
    address_line2 = models.IntegerField()
    city = models.CharField()
    state = models.CharField()
    pincode = models.IntegerField()

# class Product(models.Model):
#     # product_id = models.IntegerField()
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True,null=True)
#     price = models.DecimalField(max_digits=10,decimal_places=2)
#     unit = models.CharField(max_length=10,default="Per Kg")
#     # stock_quantity = models.IntegerField()
#     image = models.ImageField(upload_to="uploads/")
#     # is_active = models.BooleanField()
    

    # def __str__(self):
    #     return self.name

class Product(models.Model):
    name=models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")  # requires Pillow
    unit = models.CharField(max_length=50, default="Per Kg")  



    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total(self):
        return self.product.price * self.quantity