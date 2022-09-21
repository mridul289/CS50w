from django.db import models
from django.core.validators import MinLengthValidator

class Retailer(models.Model):
    retailer_ID = models.AutoField(primary_key=True)
    name = models.CharField(help_text='Retailer name', max_length=64, unique=True)
    number_1 = models.CharField(help_text='Phone number 1', max_length=10, unique=True, validators=[MinLengthValidator(10)])
    number_2 = models.CharField(help_text='Phone number 2', max_length=10, blank=True, null=True,validators=[MinLengthValidator(10)])

    def __str__(self):
        return self.name
    
    def getname(self):
        return self.name

    def getnumber(self):
        return f"{self.number_1}"



class Salesman(models.Model):
    salesman_ID = models.AutoField(primary_key=True)
    name = models.CharField(help_text="Salesman name", max_length=64, unique=True)

    def getname(self):
        return self.name

    def __str__(self):
        return self.name




class Invoice(models.Model):
    invoice_ID = models.AutoField(primary_key=True)
    retailer = models.ForeignKey(Retailer, help_text='Retailer ID', on_delete=models.CASCADE, related_name='retailer_invoices')
    amount = models.PositiveIntegerField(help_text='Amount')
    salesman = models.ForeignKey(Salesman, help_text='Salesman ID', on_delete=models.CASCADE, related_name="salesman_invoices")
    date = models.DateField(auto_now_add=True, help_text='Date')

    def __repr__(self):
        return {
            "retailer":Invoice.retailer,
            "amount":Invoice.amount,
            "date":Invoice.date
        }
    
    def getdate(self):
        return self.date

    def getamount(self):
        return self.amount