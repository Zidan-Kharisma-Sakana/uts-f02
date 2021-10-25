from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,)
    name = models.CharField(max_length=200, null=True)
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
        return ": "+self.status

class Following(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="pengikut")
    followee = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True,)
    isAccepted = models.BooleanField(default=False)

