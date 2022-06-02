
from urllib import response
from django.shortcuts import render
from django.conf import Settings, settings
from django.contrib.auth.models import User
from django.http import Http404
from html5lib import serialize
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from cart.models import Cart
from rest_framework.permissions import IsAuthenticated
from orders.models import Address, Order
from orders.serializers import AddressSerializer, OrderSerializer
from instamojo_wrapper import Instamojo
from django.conf import settings

# Create your views here.
api = Instamojo(api_key=settings.API_KEY,
auth_token=settings.AUTH_TOKEN,endpoint='https://test.instamojo.com/api/1.1/')

class OrderView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        order=Order.objects.filter(user=request.user)
        serializer=OrderSerializer(order,many=True)
        return Response(serializer.data)


    def post(self,request):
        user=request.user
        data=request.data
        cart=Cart.objects.get(user=request.user,ordered=False)
        is_amountpaid=False
        order=Order.objects.create(user=user,cart=cart,is_amountpaid=is_amountpaid)
        order.save()
        total_price=cart.total_price
        response=api.payment_request_create(
            amount=cart.total_price,
            purpose="Ecommerce Payment",
            buyer_name="Pranav Khot",
            email="pranavkhot77@gmail.com",
            redirect_url='http://127.0.0.1:8000/api/v1/order_success'
        )
        print(response)
        order_instamojo=Order.objects.get(user=user,cart=cart)
        order_instamojo.order_id=response['payment_request']['id']
        order_instamojo.instamojo_response=response
        order_instamojo.save()
        return Response({
            'status':"Order added Successfully",
            "total_price":total_price,
            'user':user.username,
            'payment_url':response['payment_request']['longurl']
        })
    def put(self,request):
        data=request.data
        order_object=Order.objects.get(id=data.get('id'))
        order_object.is_amountpaid=data.get('is_amountpaid')
        order_object.save()
        order=Order.objects.filter(user=request.user)
        serializer=OrderSerializer(order,many=True)
        return Response(serializer.data
        )
    def delete(self,request):
        data=request.data
        order_object=Order.objects.get(id=data.get('id'))
        order_object.delete()
        order=Order.objects.filter(user=request.user)
        serializer=OrderSerializer(order,many=True)
        return Response(serializer.data
        )

class AddressView(APIView):
    def get(self,request):
        address=Address.objects.filter(user=request.user)
        serializer=AddressSerializer(address,many=True)
        return  Response(serializer.data)
    def post(self,request):
        user=request.user
        data=request.data
        name=data.get('name')
        address=data.get('address')
        phone_number=data.get('phone_number')
        Address_Object=Address.objects.create(
            user=user,name=name,address=address,phone_number=phone_number
        )
        Address_Object.save()
        user_address=Address.objects.filter(user=request.user)
        serializer=AddressSerializer(user_address,many=True)
        return  Response({
            "message":"Address Saved Successfully",
            "response":serializer.data,
            })

@api_view(['GET'])   
def order_success(request):
    payment_request_id=request.query_params.get('payment_request_id')
    # print(payment_request_id)
    cart=Cart.objects.get(user=request.user,ordered=False)
    order=Order.objects.get(user=request.user,order_id=payment_request_id)
    order.is_amountpaid=True
    cart.ordered=True
    order.save()
    cart.save()
    return Response({'message':'Payment Successfull'})
