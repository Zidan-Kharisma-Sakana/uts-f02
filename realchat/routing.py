# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
  re_path(r'ws/realchat/(?P<dm_id>\w+)/$', consumers.ChatConsumer),
]