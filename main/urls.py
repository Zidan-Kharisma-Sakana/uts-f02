from django.urls import path

from . import views
from forum.views import TopicListView

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('anonymousmessage/', views.anonymous_page, name='anonymous_page'),
    path('forum/', TopicListView.as_view(), name='forum_index'),
]
