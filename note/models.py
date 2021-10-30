from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    timestamp = models.DateTimeField()
    text = models.TextField()

    def __str__(self):
        return f"{self.user.username} | {self.title}"
