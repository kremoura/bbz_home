from django.urls import path
from comum.views import index

urlpatterns = [
    path('', index, name='login')
]