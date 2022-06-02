from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from psutil import users
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from yaml import serialize

from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer
from products.models import Product
# Create your views here.

# class CartView(APIView):
#     def get(self,request):
#         try:
#             cart=Cart.objects.get(user=request.user)
#             serializer=CartGETSerializer(cart)
#             return Response(serializer.data)
#         except:
#             return Response(serializer.errors)
#     def post(self,request):
#         serializer=CartSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save(user=self.request.user)
#             return Response(serializer.data)
#         return Response(serializer.errors)
        
#     def put(self,request):
#         try:
#             cart=Cart.objects.get(user=request.user)
#             serializer=CartSerializer(cart,data=request.data,context={'request':request})
#             if serializer.is_valid():
#                 serializer.save(user=self.request.user)
#                 return Response(serializer.data)
#             return Response(serializer.errors)
#         except:
#             return Response(serializer.errors)
#     def delete(self,request):
#         cart=Cart.objects.get(user=request.user)
#         cart.delete()
#         return Response({"Success":"Deleted Successfully"})


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user=request.user
        cart=Cart.objects.filter(user=user,ordered=False).first()
        cart_items=CartItem.objects.filter(cart=cart)
        serializer=CartItemSerializer(cart_items,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        data=request.data
        user=request.user
        cart,_=Cart.objects.get_or_create(user=user,ordered=False)
        item=Product.objects.get(id=data.get('item'))
        price=item.price
        quantity=data.get('quantity')
        cartitem=CartItem(
            user=user,cart=cart,item=item,price=price,quantity=quantity
        )
        cartitem.save()
        total=0
        carts_product=CartItem.objects.filter(user=user,cart=cart.id)
        for a in carts_product:
            total+=a.price
        cart.total_price=total
        cart.save()
        return Response({"message":"Items Successfully Added"})

    def put(self,request):
        data=request.data
        cart_item=CartItem.objects.get(id=data.get('id'))
        quantity=data.get('quantity')
        cart_item.quantity+=quantity
        cart_item.save()
        cart=Cart.objects.filter(user=request.user,ordered=False).first()
        cart_items=CartItem.objects.filter(cart=cart)
        serializer=CartItemSerializer(cart_items,many=True)
        return Response(serializer.data)
    

    def delete(self,request):
        user=request.user
        data=request.data
        delete_item=CartItem.objects.get(id=data.get('id'))
        delete_item.delete()
        cart=Cart.objects.filter(user=user,ordered=False).first()
        cart_items=CartItem.objects.filter(cart=cart)
        serializer=CartItemSerializer(cart_items,many=True)
        return Response(serializer.data)
    