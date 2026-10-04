from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
    blank=True) 
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    # image = models.ImageField(upload_to='product_images',null=True, blank=True)
    file = models.FileField(upload_to='uploads')
    total_sales_amount = models.IntegerField(default=0)
    total_sales = models.IntegerField(default=0)
    category = models.CharField(max_length=100 ,null=True, blank=True)

    def __str__(self):
        return self.name

class OrderDetail(models.Model):
    customer_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()

    razorpay_payment_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    has_paid = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
