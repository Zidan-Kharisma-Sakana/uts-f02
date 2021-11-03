# chat_app/consumers.py
import json

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from user.models import Profile
from .models import DM, Pesan
from django.core import serializers

class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    print("Connected!")
    self.user = self.scope["user"]

    self.room_name = self.scope['url_route']['kwargs']['dm_id']
    self.room_group_name = 'dm_%s' % self.room_name

    print(self.user.id)
    print(self.user.email)
    print(self.user.username)
    print(self.room_name)
    print(self.room_group_name)
    print(self.channel_name)

    isAllowed= await database_sync_to_async(self.get_allowed_user)()
    if not isAllowed:
      self.close()
    
    # Join room group
    await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name
    )

    await self.accept()

  async def disconnect(self):
    await self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
    )

  # Receive message from WebSocket
  async def receive(self, text_data):
    self.received_data = json.loads(text_data)
    print(self.received_data)
    print(text_data)

    if self.received_data['isi'] == 'get-history':
      room_messages = await database_sync_to_async(self.get_messages)()
      print("get-history")

      await self.send(text_data=json.dumps({
        'message': {'type':'get-history', 'history': room_messages}
      }))

    else:
      await database_sync_to_async(self.save_messages)()
      print("save messages")
  
      # Send message to room group
      await self.channel_layer.group_send(
          self.room_group_name,
          {
              'type': 'chat_message',
              'message': self.received_data
          }
      )

  def get_messages(self):
      # if room exists get messages
      room = DM.objects.get(id=self.room_name)
      messages = room.pesan_set.select_related('pengirim', 'penerima').all()
      print(messages)
      for message in messages:
        print(message)
        print(message.isi)
        print(message.penerima)
        print(message.pengirim)
      s = [{'isi': message.isi, 'penerima':message.penerima.name, 'pengirim':message.pengirim.name } for message in messages]
      print(s)
      return s
  
  def get_allowed_user(self):
    user_profile = User.objects.get(id=self.user.id)
    dm = DM.objects.get(id=self.room_name)
    return dm.pengundang == user_profile or dm.diundang == user_profile


  def save_messages(self):
    data = self.received_data.get('isi', '')
    sender = Profile.objects.get(name=self.user.username)
    dm = DM.objects.get(id=self.room_name)
    if dm.pengundang != sender:
      penerima = dm.pengundang
    else:
      penerima = dm.diundang
    Pesan.objects.create(isi=data,penerima=penerima, pengirim=sender,dm_id=dm)
    print("created message, saved in Pesan")

  # Receive message from room group
  async def chat_message(self, event):
    message = event['message']
    print('chat_message')
    print(message)
    print(event)

    # Send message to WebSocket
    await self.send(text_data=json.dumps({
        'message': {'type':'send-message', 'isi':message}
    }))