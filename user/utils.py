from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.template.loader import render_to_string

def createEmail(request, user):
    current_site = get_current_site(request)
    email_subject = 'Active your Account'
    email_context= render_to_string('user/activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': PasswordResetTokenGenerator().make_token(user)})
    return {
        'subject': email_subject,
        'message': email_context
    }

generate_token = PasswordResetTokenGenerator()