from django.urls import path
from .views import *
urlpatterns = [
    path('order/',OrderView.as_view()),
    path('user_address/',AddressView.as_view()),
    path('order_success/',order_success,name='order_success')
]
