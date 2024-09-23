from django.shortcuts import render

def index(request):
    return render(request, 'comum/sign-in/signin.html')