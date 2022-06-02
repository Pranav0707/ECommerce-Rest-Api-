import imp
from django.urls import path,include
from .views import AuthenticationView, CategoryDetail, CategoryWiseProducts, ProductDetail, ProductsList,create_category,create_product

urlpatterns=[
    path('products_list/',ProductsList.as_view()),
    path('products_detail/<slug:category_slug>/<slug:product_slug>/',ProductDetail.as_view()),
    path('category_detail/<slug:category_slug>/',CategoryDetail.as_view()),
    path('create_category/',create_category),
    path('create_product/',create_product),
    path('authenticationview/',AuthenticationView.as_view(),),
    path('categorywiseproducts/<slug:category_slug>',CategoryWiseProducts.as_view())
]