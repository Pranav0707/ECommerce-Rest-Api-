from django.http import Http404
from .serializers import CategorySerializer, CreateProductSerializer, ProductSerializer,CreateCategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product,Category
from rest_framework.decorators import api_view
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class ProductsList(APIView):
    def get(self,request,format=None):
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self,category_slug,product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            return Http404
        
    def get(self,request,category_slug,product_slug,format=None):
        product=self.get_object(category_slug,product_slug)
        serializer=ProductSerializer(product,many=False)
        return Response(serializer.data)
    

class CategoryDetail(APIView):
    def get_object(self,category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            return Http404
    
    def get(self,request,category_slug,format=None):
        category=self.get_object(category_slug)
        serializer=CategorySerializer(category)
        return Response(serializer.data)

@api_view(['POST'])
def search(request):
    search_data=request.data.get('search_data',"")

    if search_data:
        products=Product.objects.filter(Q(name__icontains=search_data)|Q(description__icontains=search_data))
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)
    else:
        return Response({"products":[]})

@api_view(['POST'])
def create_category(request):
    serializer=CreateCategorySerializer(data=request.data)
    categories=Category.objects.all()
    if serializer.is_valid():
            serializer.save()
    return Response(data=serializer.data)

@api_view(['POST']) 
def create_product(request):
    serializer=CreateProductSerializer(data=request.data)
    if serializer.is_valid():
        print("true")
        serializer.save()
        return Response(data=serializer.data)
    else:
        return Response(data=serializer.errors)


class AuthenticationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        return Response({'message':'Authenticated!!!'})

class CategoryWiseProducts(APIView):
    def get(self,request,category_slug):
        product=Product.objects.filter(category__slug=category_slug)
        serializer=ProductSerializer(product,many=True)
        return Response(serializer.data)