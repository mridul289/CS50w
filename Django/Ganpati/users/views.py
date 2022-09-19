from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *
from django.contrib.auth import authenticate, login, logout

class LoginForm(forms.Form):

    username = forms.CharField(label='Username')
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))    

#---------------------------------------------------------------------------------


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "users/index.html")

def login_func(request):
    context = {
        "loginform":LoginForm()
    }

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username = username, password = password)
            if not user == None:
                login(request, user)
                return HttpResponseRedirect(reverse('notifier:invoicepage'))
            else:
                return render(request, "users/login.html", {**context, **{"message":"Invalid credentials"}})

    return render(request, "users/login.html", context)

def logout_func(request):
    logout(request)
    return render(request, "users/login.html", {
        "loginform":LoginForm(),
        "message" : "Logged out."
    })
