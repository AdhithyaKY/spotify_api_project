from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'landing/home.html')


def about(request):
    return render(request, 'landing/about.html')
