from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'sender/main.html')

def dashboard(request, name):
    return render(request, 'sender/dashboard.html', {
        "name": name.capitalize(),
    })
