from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="anonymsg"),
    path("list-message", views.MyAnonymousView.as_view(), name="anonymous-page"),
    path("edit-message", views.edit_message, name="edit-message"),
    path(
        "list-message/<str:name>",
        views.OtherAnonymousView.as_view(),
        name="anonymous-page-other",
    ),
    path("ask-page/<str:name>", views.AskView.as_view(), name="ask-page"),
]
