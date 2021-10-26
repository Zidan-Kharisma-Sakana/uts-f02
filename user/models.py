from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,)
    name = models.CharField(max_length=200, unique=True, null=True)
    email = models.EmailField()
    birthday = models.DateField(null=True)
    bio = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class UserStatus(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    status = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
    liker = models.ManyToManyField('Profile', related_name="liked_status")

    def __str__(self):
        return self.user.name+": "+self.status

class Invitation(models.Model):
    inviter = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="diundang")
    invitee = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True,related_name="pengundang")
    isAccepted = models.BooleanField(default=False)
    message = models.CharField(max_length=200, default="Hi! Let's be friend", null=True)
    def __str__(self):
        return self.inviter.name+" invites "+self.invitee.name

