from django.shortcuts import render
from django.http import HttpResponse

def index_log(request):
    return render(request, 'log/index.html')