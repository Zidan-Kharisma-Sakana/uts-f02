from django.http import request
from django.http.response import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, views as auth_views
from django import forms
from django.urls.base import reverse_lazy
from .forms import CreateUserForm, MyAuthenticationForm
from django.views import View
from threading import Thread
from .utils import createEmail
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from django.utils.dateparse import parse_date

class MyThread(Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        Thread.__init__(self)
    def run(self):
        self.email_message.send()

class MyCreateUserView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, 'user/create_account.html', context={
            'form': form
        })
    def post(self, request):
        data = request.POST
        print("---------aaadqS-------")
        form = CreateUserForm(data)
        print("-------aa---------")

        if form.is_valid():
            user = form.save()
            email_content = createEmail(request, user)
            email_message = EmailMessage(
                email_content['subject'],
                email_content['message'],
                settings.EMAIL_HOST_USER,
                [data.get('email')]
            )
            MyThread(email_message).start()
            return render(request, 'user/check_email.html')

        print(form.errors)
        print(form.error_messages)
        return render(request, 'user/create_account.html', context={
            'form': form,
            'has_error': True
        })


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            name = getattr(user, 'username')
            email = getattr(user, 'email')
            print("------------")
            print(name)
            print(email)
            user_profile = models.Profile(user=user, name=name, email=email)
            user_profile.save()
            return render(request, 'user/activate_success.html')
        return render(request, 'user/activate_fail.html', status=401)

class MyUserLoginView(auth_views.LoginView):
    template_name= 'user/login.html'
    extra_context = {
        'dataX': 'hai'
    }
    authentication_form = MyAuthenticationForm

    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        elif self.request.user.is_superuser:
            return "/admin/"
        else:
            return reverse("user")

class MyLogoutView(auth_views.LogoutView):
    next_page=reverse_lazy('login')
        
class MyChangePassword(LoginRequiredMixin, auth_views.PasswordChangeView):
    login_url = reverse_lazy('login')
    template_name='user/change-password.html'
    success_url = reverse_lazy('user')

class MyPasswordResetView(auth_views.PasswordResetView):
    template_name='user/reset-password.html'
    email_template_name='user/reset.html'
    subject_template_name='user/password_reset_subject.txt'

class MyPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name='user/password_reset_done.html'

class MyPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name='user/password_reset_confirm.html'

class MyPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name='user/password_reset_complete.html'

