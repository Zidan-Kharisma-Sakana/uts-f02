from django.urls import path
from .views import *

app_name = "note"

urlpatterns = [
    path("", index, name="index"),
    path('add_message/', add_message, name="add_message"),
    
]
