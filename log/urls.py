from django.urls import path
from log.views import index_log

urlpatterns = [
    path('', index_log)
]