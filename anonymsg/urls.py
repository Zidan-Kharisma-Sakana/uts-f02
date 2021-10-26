from django.urls import path
from . import views

urlpatterns = [
    path("", views.anonymous_page, name="anonymous-page"),
    path("edit-message", views.edit_message, name="edit-message"),
    path("no-message", views.edit_message, name="no-message"),
    path("ask-page", views.ask_page, name="ask-page"),
]
