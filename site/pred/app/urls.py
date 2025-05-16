# app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('journal/', views.journal, name='journal'),
    path('resources/', views.resources, name='resources'),
]