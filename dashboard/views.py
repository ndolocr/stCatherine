from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def dashboardIndex(request):
    return  HttpResponse("Dashbaord-Tatiana")