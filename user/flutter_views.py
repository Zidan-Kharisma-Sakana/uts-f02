from django.contrib.auth.models import User
from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY, authenticate, login, logout
from django.http import JsonResponse, response
import json
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from time import sleep
from .models import Profile

@csrf_exempt
def profile_flutter(request, username):
    print(username+"-------")
    # data = json.loads(request.body)
    user = User.objects.get(username=username)
    sleep(1)
    if user is not None:
        print(user.email)
        profile = Profile.objects.get(user=user)        
        bod = profile.birthday

        return JsonResponse({
            "username": username,
            "bod": profile.birthday or "belum diatur",
            "bio": profile.bio or "belum diatur",
            "email": profile.email
        }, status=200)
    else:
        return JsonResponse({}, status=404)

@csrf_exempt
def edit_profile_flutter(request):
    data = json.loads(request.body)
    username=data['username']
    user = User.objects.get(username=username)
    print(data['bod'])
    sleep(1)
    # return JsonResponse({}, status=200)
    if user is not None:
        user_profile = Profile.objects.get(user=user)  # Mendapatkan profile berdasarkan user
        user_profile.birthday = parse_date(data['bod'][:10])
        user_profile.bio = data['bio']
        user_profile.save() 
        return JsonResponse({}, status=200)
    else:
        return JsonResponse({}, status=404)

@csrf_exempt
def login_flutter(request):
    data = json.loads(request.body)
    username = data["username"]
    password = data["password"]
    print(username+"  "+password)
    user = authenticate(username=username, password=password)
    print(user)
    if user is not None:
        email = User.objects.get(username=username).email
        return JsonResponse({"logged": True, "username":username, "email": email, 'message': "Anda telah berhasil masuk :)"}, status=200)
    else:
        return JsonResponse({"logged": False, "message": "Perhatikan username dan password kamu!"}, status=404)

@csrf_exempt
def register_flutter(request):
    data = json.loads(request.body)
    username = data["username"]
    password = data["password"]
    email = data['email']
    usr = User.objects.filter(username= username) #this is stupid
    if(usr.count()>0):
        return JsonResponse({"message":"Sudah ada yang menggunakan username '"+username+"' :("}, status=503)
    eml = User.objects.filter(email=email)
    if(eml.count()>0):
        return JsonResponse({"message":"Sudah ada yang menggunakan email '"+email+"' :("}, status=503)
    try:
        user = User.objects.create_user(username=username,
                                 email=email,
                                 password=password)
        profile = Profile.objects.create(user=user, name=username, email=email)
        return JsonResponse({"message":"Selamat, pendaftaran berhasil. Cek email verifikasi di '"+email+"' :("}, status=200)
    except Exception as e:
        return JsonResponse({"message":e}, status=404)
