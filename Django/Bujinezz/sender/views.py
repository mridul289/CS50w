from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'sender/main.html')

def subject(request, subjectname):
    return HttpResponse(f"This is {subjectname}!")