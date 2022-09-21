from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse_lazy, reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *
import requests
from requests.structures import CaseInsensitiveDict
from dal import autocomplete
from datetime import date
from django.template.defaulttags import register

def whatsapp_send(number, salesman, amount):
    url = "https://graph.facebook.com/v14.0/101165502755328/messages"
    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer xxxxxxxx"
    headers["Content-Type"] = "application/json"
    data = '{ "messaging_product": "whatsapp", "to": "91' + str(number) + '", "type": "template", "template": { "name": "notifier_message", "language": { "code": "en_US" }, "components": [ { "type": "body", "parameters": [ { "type": "text", "text": "' + salesman + '" }, { "type": "text", "text": "' + str(amount) + '" } ] } ] } }'
    resp = requests.post(url, headers=headers, data=data)
    print(resp.status_code)
    return resp.status_code

#-------------------------Autocomplete-------------------------------

class RetailerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return Invoice.objects.none()

        qs = Retailer.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

#-------------------------Forms-------------------------------

class InvoiceForm(forms.Form):
    retailer = forms.ModelChoiceField(queryset=Retailer.objects.all(), required=True, widget=autocomplete.ModelSelect2(url='retailer-autocomplete'))
    amount = forms.IntegerField(label="Amount accepted", min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))              #submit button

class RetailerForm(forms.Form):
    retailer = forms.CharField(label="Retailer Name", max_length=64)
    number_1 = forms.CharField(label="1nd Number", required=True, max_length=10, min_length=10)
    number_2 = forms.CharField(label="2nd Number", required=False, max_length=10, min_length=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))              #submit button


#---------------------Filters-----------------------------------

@register.filter(name="diction")
def get_item(dictionary, key):
    return dictionary[key]

#---------------------Main Views-----------------------------------

def index(request):                                                #Page to enter the invoice
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    
    context = {
        'invoiceform' : InvoiceForm(),
        'user' : str(request.user)
    }

    if request.method == 'POST' :
        iform = InvoiceForm(request.POST)
        if iform.is_valid():
            curr_retailer = Retailer.objects.get(name = str(iform.cleaned_data["retailer"]))
            curr_amount = int(iform.cleaned_data["amount"])
            salesman = str(request.user)
            try:
                curr_invoice = Invoice(retailer = curr_retailer, amount= curr_amount, salesman= Salesman.objects.get(name = salesman))
            except:
                return render(request, "notifier/error.html")
            curr_invoice.save()
            hi = whatsapp_send(curr_retailer.number_1, salesman, curr_amount)
            
            return render(request, "notifier/index.html", {**context, **{
                "current_invoice": curr_invoice,
                "status":hi
                }})
        else: 
            return HttpResponse("NONE")

    return render(request, "notifier/index.html", context)          #on load

def today(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))

    retailer_dict = {}
    retailers = list(Retailer.objects.all().values('retailer_ID', 'name'))
    for i in retailers:
        retailer_dict[i['retailer_ID']] = i['name']

    context = {
        "Invoices":Invoice.objects.filter(salesman = Salesman.objects.get(name = request.user), date = date.today()).values(),
        "retailers":retailer_dict
    }

    return render(request, "notifier/today.html", context)

def addretailer(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    
    context= {
        "retailerform": RetailerForm(),
        'user': str(request.user)
    }

    if request.method == 'POST':
        rform = RetailerForm(request.POST)
        if rform.is_valid():
            curr_retailer = str(rform.cleaned_data["retailer"])
            number = str(rform.cleaned_data["number_1"])
            try:
                numb = str(rform.cleaned_data["number_2"])
            except:
                numb = None
            created_retailer = Retailer(name= curr_retailer, number_1=  number, number_2= numb)
            created_retailer.save()

            return render(request, "notifier/add.html", {**context, **{
                "current_retailer": created_retailer
                }})
        
        else:
            return render(request, "notifier/error.html", {"form", rform.cleaned_data})
        
    return render(request, "notifier/add.html", context)