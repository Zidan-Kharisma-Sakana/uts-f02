from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.template.loader import render_to_string
from . import models
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

def updateInvitation(inviter, invitee, isDelete ):
    invitation = models.Invitation.objects.filter(inviter=inviter, invitee=invitee)
    if invitation.count()>0:
        if isDelete:
            invitation[0].delete()
        else:
            invitation1 = models.Invitation.objects.get(inviter=inviter, invitee=invitee)
            invitation1.isAccepted = True
            invitation1.save()