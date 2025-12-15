from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse('<h1>Home-PROJECT MANAGEMENT SYSTEM</h1> <br> <h4> VERSION : 1.0 </h4>')