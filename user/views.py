from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import models
from django.utils.dateparse import parse_date

@login_required(login_url='/user/login/')
def home(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin/')
    
    user_id = request.user.id # Mendapatkan id user 
    user = User.objects.get(id=user_id) #mencari objek user berdasarkan id user
    print(user.profile)
    return render(request, 'user/profile.html', {
        'profile': user.profile
    })

@login_required(login_url='/user/login/')
def edit_profile(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin/')

    user_id = request.user.id        # Mendapatkan id user 
    user = User.objects.get(id=user_id)      #mencari objek user berdasarkan id user
    data = request.POST               # data adalah dictionary yang key-valuenya adalah nama input dan isinya 
    print(data) 

    if(request.method == 'POST'):    # Akan dijalankan bila methodnya POST
        user_profile = models.Profile.objects.get(user=user)  # Mendapatkan profile berdasarkan user
        print(user_profile)
        user_profile.name = data['name']      # Mengset field name dengan data baru
        user_profile.birthday = parse_date(data['birthday'])
        user_profile.bio = data['bio']
        user_profile.save() # Menyimpan kembali objek profile 
        return HttpResponseRedirect('/user') # Meredirect


    return render(request, 'user/edit-profile.html', {
        'profile': user.profile
    })