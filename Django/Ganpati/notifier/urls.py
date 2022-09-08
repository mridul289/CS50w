from django.urls import path
from . import views
from django.shortcuts import render

app_name = 'notifier'

urlpatterns = [
    path("", views.index, name="loginpage"),
    path("invoice", views.invoice, name="invoice"),
]