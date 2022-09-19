from django.urls import path
from . import views

app_name = 'notifier'

urlpatterns = [
    path("", views.index, name="invoicepage"),
    path("invoices", views.invoices_list, name="invoices_list"),
    path("add", views.addretailer, name="addretailer")
]