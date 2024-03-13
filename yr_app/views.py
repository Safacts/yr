from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def homepage(request):
    return render(request,"yrcorporation.html")

def products(request):
    return render(request,"products.html")