from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ValidationError, EmailField

from user import models


class MyAuthenticationForm(AuthenticationForm):
    """"
    Overide method clean from AuthenticationForm to show that a user hasn't activate their account
    """
    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': ("This Account hasn't been activated yet, Please check your email  :)"),
    }
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                print(username)
                try:
                    user_temp = User.objects.get(username=username)
                except:
                    user_temp = None
                print(user_temp)
                if user_temp is not None:
                        self.confirm_login_allowed(user_temp)
                else:
                    raise ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )

        return self.cleaned_data


class CreateUserForm(UserCreationForm):
    """"
    Override UserCreationForm to include email field
    """
    email = EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    error_messages = {
        'password_mismatch': ('The two password fields didn’t match.'),
        'email_taken': 'Your email has been taken'
    }

    def clean_email(self):
        """
        Check if the email had already been taken
        """
        email = self.cleaned_data.get('email')
        num = User.objects.filter(email=email)
        if  num.count() > 0:
            raise ValidationError(
                self.error_messages['email_taken'],
                code='email_taken',
            )

        return email

    def save(self, commit= True):
        user = super(CreateUserForm, self).save(commit=False)
        email = self.cleaned_data.get('email')
        user.email = email
        user.is_active=False
        if commit:
            user.save()
        return user
