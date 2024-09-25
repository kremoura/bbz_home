from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cadastro.urls')),
    path('', include('comum.urls')),
    path('', include('prestacao_contas.urls')),
]
