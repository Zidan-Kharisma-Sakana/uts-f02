from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.urls import reverse
from user import forms
from . import models
from django.utils.dateparse import parse_date
from django.http.response import Http404, HttpResponse
from django.core import serializers


@login_required(login_url='/user/login/')
def home(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin/')
    return HttpResponseRedirect(reverse('status'))    

    user_id = request.user.id # Mendapatkan id user 
    # user = User.objects.get(id=user_id) #mencari objek user berdasarkan id user
    # print(user.profile)
    # return render(request, 'user/profile.html', {
    #     'profile': user.profile
    # })

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

class LikeStatusView(LoginRequiredMixin, View):
    def post(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        status_id = request.POST.get('status_id')
        status = models.UserStatus.objects.get(id=status_id)
        liker = status.liker
        print("----")
        liker_filtered = liker.filter(user=user)
        print("----")
        if liker_filtered.count() > 0:
            print("---ss-")
            isDislike=True
            liker.remove(user.profile)
            print("----")

        else:
            isDislike=False
            print("----")
            liker.add(user.profile)
            print("----")
        totalCount = status.liker.all().count()
        json_object = JsonResponse({"isDislike":isDislike, "totalCount": totalCount})
        return json_object

  
class OtherStatusView(LoginRequiredMixin, View):
    def get(self, request, name):
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        try:
            user_id = request.user.id
            user_profile = User.objects.get(id=user_id).profile
            if name == user_profile.name:
                return HttpResponseRedirect(reverse('status'))
            status_owner = models.Profile.objects.get(name=name)
            data = list_status(status_owner, user_profile)
        except:
            return Http404()
        return render(request, 'user/profile/status.html', {
            'data': data,
            'form': False,
            'owner': status_owner.name,
            'dataProfile': status_owner
        })

class MyStatusView(LoginRequiredMixin, View):
    def post(self,request):
        print("skreeeeee")
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        user_id = request.user.id
        user = User.objects.get(id=user_id).profile
        data = request.POST
        flag = True
        if data['status'] is None or data['status'] == '':
            flag = False
        if user is not None and flag:
            status = models.UserStatus(user=user, status=data['status'])
            status.save()
            return HttpResponseRedirect(reverse('status'))
        data = list_status(user)        
        return render(request, 'user/profile/status.html', {
            'has_error': True,
            'data': data,
            'dataProfile':  user,
            'form': True
        })

    def get(self, request):
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        user_id = request.user.id
        user = User.objects.get(id=user_id).profile
        data = list_status(user, user)
        print(data)
        return render(request, 'user/profile/status.html', {
            'data': data,
            'form': True,
            'dataProfile':  user,
            'has_error': False
        })

def list_status(status_owner, user):
    status_list = models.UserStatus.objects.filter(user=status_owner).order_by('-time')
    data = []
    print(status_list)
    for status in status_list:
        likes = status.liker.all().count()
        isLiked = user.liked_status.filter(id=status.id).count() > 0
        datum = {
            'name': status_owner.name,
            'status_id': status.id,
            'status': status.status,
            'time': status.time,
            'likes': likes,
            'isLiked': isLiked
        }
        data.append(datum)
    return data