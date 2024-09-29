from django.urls import path
from apis.views import buscar_emails

urlpatterns = [
    path('api/', buscar_emails, name='buscar_emails'),
]