from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class NoteModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=13)
    timestamp = models.DateField(null=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.user.username} | {self.title}"
