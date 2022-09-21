from django.urls import path
from . import views

app_name = 'notifier'

urlpatterns = [
    path("", views.index, name="invoicepage"),
    path("add", views.addretailer, name="addretailer"),
    path("today", views.today, name="today")
]