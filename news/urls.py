from django.urls import path
from . import views

urlpatterns = [
    path('', views.newshome, name='newshome'),
    path('newsreq/', views.newsrequest, name='newsrequest'),
]