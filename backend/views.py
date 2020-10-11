from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.

def home(request):
    return HttpResponse(
        "<h1>Adusermizer</h1> \
        <p>A proof-of-concept app for UAS thesis to manage Active Directory users in an environment of multiple independent AD:s wihtout \
            trust relations."
        )