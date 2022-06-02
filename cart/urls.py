from django.urls import path
from .views import *
urlpatterns = [
    path('cartview/',CartView.as_view()),
]
