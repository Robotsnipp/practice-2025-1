# app/views.py

from django.shortcuts import render

def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request, 'app/about.html')

def team(request):
    return render(request, 'app/team.html')

def journal(request):
    return render(request, 'app/journal.html')

def resources(request):
    return render(request, 'app/resources.html')