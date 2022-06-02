from operator import mod
from django.db import models
from django.contrib.auth.models import User
from cart.models import Cart
from products.models import Product
# # Create your models here.

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")
    is_amountpaid=models.BooleanField(default=False)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    order_id=models.CharField(max_length=200,blank=True)
    instamojo_response=models.TextField(blank=True,null=True)

    class Meta:
        ordering=["-created_at",]

    def __str__(self):
        return self.user.username
    


class OrderItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,related_name="order_item",on_delete=models.CASCADE)

    class Meta:
        ordering =["-id",]

    # def get_cost(self):
    #     return self.price * self.quantity

class Address(models.Model):
    name=models.CharField(max_length=100)
    address=models.TextField()
    phone_number=models.CharField(max_length=15)
    user=models.ForeignKey(User,on_delete=models.CASCADE)


