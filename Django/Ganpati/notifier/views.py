from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse_lazy, reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


USERS = (
    ("Mridul","Mridul"),
    ("Tanay","Tanay"),
    ("Aman","Aman")
)

PASSWORDS = {
    "Mridul":"vleviosa",
    "Tanay":"gundumundu",
    "Aman":"j.a.d.u."
}

class LoginForm(forms.Form):

    user = forms.ChoiceField(label='Username', choices=USERS)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))              #submit button


class InvoiceForm(forms.Form):

    retailer = forms.CharField(label='Retailer')
    amount = forms.IntegerField(label="Amount accepted", min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))              #submit button

#---------------------------------------------------------------------------

def index(request):
    context = {
        'loginform':LoginForm(),
    }
    invalid_pass = { 'invalid':True }

    if "invoices_list" not in request.session:
        request.session["invoices_list"] = []

    if request.method == 'POST':                                    #accept and check the form submit request
        lform = LoginForm(request.POST)
        if lform.is_valid():
            user = lform.cleaned_data["user"]
            password = lform.cleaned_data["password"]
            if password == PASSWORDS[user]:                         #if correct password
                return HttpResponseRedirect(reverse("notifier:invoice"))
            else:                                                   #if invalid password
                return render(request, "notifier/index.html", {**context, **invalid_pass})

    return render(request, "notifier/index.html", context)          #on load

def invoice(request):
    context = {
        'invoiceform':InvoiceForm(),
        'invoices_list':request.session["invoices_list"],
    }

    if request.method == "POST":
        iform = InvoiceForm(request.POST)
        if iform.is_valid():
            retailer = str(iform.cleaned_data["retailer"])
            amount = iform.cleaned_data["amount"]
            request.session["invoices_list"] += [(retailer, amount)]
            return HttpResponseRedirect(reverse("notifier:invoice"))
        else:
            render(request, "notifier/invoice.html", context)

    return render(request, "notifier/invoice.html", context)
