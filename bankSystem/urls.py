from django.urls import path, include
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),  # For login/logout
    # OpenAPI schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI

    # Your app URLs
    path('api/BankAccount/', include('BankAccount.urls')),
    path('api/BankBalance/', include('BankBalance.urls')),
    path('api/Loan/', include('Loan.urls')),
    path('api/Transaction/', include('Transaction.urls')),
    path('api/User/', include('User.urls')),
]
