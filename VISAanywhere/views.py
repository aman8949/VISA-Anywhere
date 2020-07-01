from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')