from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from user_accounts.views import Register
urlpatterns=[
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user_registration/',Register.as_view(),),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]