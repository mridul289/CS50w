from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('retailer', 'amount', 'salesman', 'date')


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Retailer)
admin.site.register(Salesman)
