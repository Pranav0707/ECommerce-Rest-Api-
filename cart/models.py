from django.http import JsonResponse
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

from products.models import Product
# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    items_in_cart=models.IntegerField(default=0)
    total_price=models.FloatField(default=0)
    ordered=models.BooleanField(default=False)

    def __str__(self):
        return f"Cart has {self.total_price} items of User:{self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name="items", default=None)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    price=models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    

    # def __str__(self):
    #     return str(self.id)

@receiver(pre_save, sender=CartItem)
def price_updation(sender, **kwargs):
    cart_items=kwargs['instance']
    product_price=Product.objects.get(id=cart_items.item.id)
    cart_items.price=cart_items.quantity *float(product_price.price)
    print(cart_items.price)
