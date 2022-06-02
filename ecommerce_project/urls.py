
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    #for djoser authentication
    # path("api/v1/", include('djoser.urls')),
    # path("api/v1/", include('djoser.urls.authtoken')),
    path("api/v1/", include('products.urls')),
    path("api/v1/", include('user_accounts.urls')),
    path("api/v1/", include('cart.urls')),
    path("api/v1/", include('orders.urls')),
    # path("payments/instamojo/", include("drf_instamojo.urls")),
    path('openapi', get_schema_view(
            title="Ecommerce Django Rest Framework",
            description="Ecommerce API",
            version="1.0.0"
        ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(template_name='swagger-ui.html',extra_context={'schema_url':'openapi-schema'}), name='swagger-ui'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

