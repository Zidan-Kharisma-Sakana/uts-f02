from django.urls import re_path

from . import consumer

websocket_urlpatterns = [
  re_path(r"ws/chatrooms/(?P<roomname>\w+)/$", consumer.ChatConsumer),
] 