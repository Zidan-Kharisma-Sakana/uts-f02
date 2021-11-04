from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
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
from .utils import updateInvitation, list_status
import user


@login_required(login_url='/user/login/')
def home(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin/')
    return HttpResponseRedirect(reverse('status'))    

@login_required(login_url='/user/login/')
def edit_profile(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin/')

    user_id = request.user.id        # Mendapatkan id user 
    user = User.objects.get(id=user_id)      #mencari objek user berdasarkan id user
    data = request.POST               # data adalah dictionary yang key-valuenya adalah nama input dan isinya 

    if(request.method == 'POST'):    # Akan dijalankan bila methodnya POST
        user_profile = models.Profile.objects.get(user=user)  # Mendapatkan profile berdasarkan user
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
        liker_filtered = liker.filter(user=user)
        if liker_filtered.count() > 0:
            isDislike=True
            liker.remove(user.profile)

        else:
            isDislike=False
            liker.add(user.profile)
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

# create invitation
class CreateInvitationView(LoginRequiredMixin, View):
    def post(self, request, name):
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        user_id = request.user.id
        inviter = User.objects.get(id=user_id).profile
        if name == inviter.name:
            return HttpResponseRedirect(reverse('status'))
        invitee = models.Profile.objects.get(name=name)
        data = request.POST
        print(data)
        message = data.get('message')
        if message == '':
            message = 'Hi! Nice to meet you'
        if len(message) > 200:
            message = message[0:200]
        count1 = models.Invitation.objects.filter(inviter=inviter, invitee=invitee).count()
        count2 = models.Invitation.objects.filter(inviter=invitee, invitee=inviter).count()
        if count1 == 0 and count2 == 0:
            new_invitation = models.Invitation(inviter=inviter, invitee=invitee, message=message)
            new_invitation.save()
        return HttpResponseRedirect(reverse('friends'))

# see friends, accept invitation, decline 
# invitation, retract invitation
class FriendsView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        
        user_id = request.user.id
        user_profile = User.objects.get(id=user_id).profile
        user_name= user_profile.name

        pending_invitation = []
        pending_invitation_querySet = models.Invitation.objects.select_related('invitee').filter(inviter=user_profile, isAccepted=False)
        for invitation in pending_invitation_querySet:
            pending_invitation.append({'message':invitation.message, 'name':invitation.invitee.name})

        inbox_invitation=[]
        inbox_invitation_querySet = models.Invitation.objects.select_related('inviter').filter(invitee=user_profile, isAccepted=False)
        for invitation in inbox_invitation_querySet:
            inbox_invitation.append({'message':invitation.message, 'name':invitation.inviter.name})
        
        friends = []        
        friends_querySet = models.Invitation.objects.select_related('inviter', 'invitee').filter(invitee=user_profile, isAccepted=True) | models.Invitation.objects.filter(inviter=user_profile, isAccepted=True)
        for invitation in friends_querySet:
            val = {}
            inviter_name = invitation.inviter.name
            if inviter_name != user_name:
                val['name'] = inviter_name
                status = invitation.inviter.posted_status.all().order_by('-time')
                val['latest'] = status[0].status if status.count() > 0 else False
            else:
                val['name'] = invitation.invitee.name
                status = invitation.invitee.posted_status.all().order_by('-time')
                val['latest'] =  status[0].status if status.count() > 0 else False
            friends.append(val)
        
        print(friends)

        return render(request, 'user/profile/friends.html', {
            'pending_invitation': pending_invitation,
            'friends': friends,
            'inbox_invitation':inbox_invitation,
            'name': user_profile,
        })

    def post(self, request):
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        user_id = request.user.id
        user_profile = User.objects.get(id=user_id).profile
        method = request.POST.get('_method') 
        if method is None:
            return
        
        target_name = request.POST.get('name')
        target_profile = models.Profile.objects.get(name=target_name)
        # To delete invitation sent
        print("---------")
        if method == 'delete':
            updateInvitation(user_profile, target_profile, True)
            return HttpResponseRedirect(reverse('friends'))
        if method == 'accept':
            # to accept invitation
            updateInvitation(target_profile, user_profile, False)
            return HttpResponseRedirect(reverse('friends'))
        # To decline invitation or delete friend
        if method == 'decline':
            updateInvitation(target_profile, user_profile, True)
            return HttpResponseRedirect(reverse('friends'))
        # to delete friend
        updateInvitation(user_profile, target_profile, True)
        updateInvitation(target_profile, user_profile, True)
        return HttpResponseRedirect(reverse('friends'))

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

class SearchFriendView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        return render(request, 'user/search/search-friend.html', {
            'name':'',
            'user': False,
        })        
    def post(self, request):
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        user_id = request.user.id
        user = User.objects.get(id=user_id).profile
        searched = request.POST.get('name')
        if searched is None:
            searched=""
        users = models.Profile.objects.filter(name__icontains=searched).order_by("name")
        users_list = []
        for user in users:
            bio = user.bio if user.bio else "-"
            users_list.append({'name': user.name,'bio': bio})

        return JsonResponse({'data': users_list})

