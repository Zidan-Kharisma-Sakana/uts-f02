# chat_app/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:dm_id>/', views.rooms, name='rooms'),
]