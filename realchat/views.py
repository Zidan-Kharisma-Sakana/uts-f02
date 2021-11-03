from django.http.response import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
import string
from user.models import Profile, Invitation
from django.contrib.auth.models import User
from .models import Pesan, DM

# Create your views here.
def index(request):
    user_id = request.user.id        # Mendapatkan id user 
    user_profile = User.objects.get(id=user_id).profile      #mencari objek user berdasarkan id user
    DMs = []        
    DM_querySet = DM.objects.select_related('pengundang', 'diundang').filter(pengundang=user_profile) | DM.objects.select_related('pengundang', 'diundang').filter(diundang=user_profile)
    for dm in DM_querySet:
        dm_data = {'name':'', 'dm_id': dm.id}
        if dm.pengundang != user_profile:
            dm_data['name'] = dm.pengundang.name
        else:
            dm_data['name'] = dm.diundang.name
        DMs.append(dm_data)
    return render(request, 'dm/index.html', {
        'DMs': DMs,
        'no_friends': len(DMs) == 0
    })

def rooms(request,dm_id):
    user_id = request.user.id        # Mendapatkan id user 
    user_profile = User.objects.get(id=user_id).profile      #mencari objek user berdasarkan id user
    # dm_room1 = DM.objects.select_related('diundang', 'pengundang').filter(pengundang=user_profile) | DM.objects.select_related('diundang', 'pengundang').filter(diundang=user_profile) 
    try:
        dm_room = DM.objects.get(id=dm_id)
    except:
        return Http404()

    if dm_room.pengundang != user_profile and dm_room.diundang != user_profile:
        return HttpResponseForbidden()
    
    if dm_room.pengundang == user_profile:
        nama_teman= dm_room.diundang.name
        nama_saya= dm_room.pengundang.name
    else:
        nama_teman= dm_room.pengundang.name
        nama_saya= dm_room.diundang.name

    return render(request, 'dm/rooms.html', {
    'dm_id': dm_id,
    'nama_teman': nama_teman,
    'nama_saya': nama_saya
    })
