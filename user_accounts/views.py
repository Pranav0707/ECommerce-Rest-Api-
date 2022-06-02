from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

class Register(APIView):
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        user=User(username=username,password=password)
        user.save()
        refresh = RefreshToken.for_user(user)

        return Response({
        "message":"User Created Succesfully",
        "user":user.username,
        "user_id":user.id,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        })
