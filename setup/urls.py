from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('log/', include('log.urls')),
    path('atualizacao_cadastral/', include('atualizacao_cadastral.urls'))
]
