from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    checklist = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(default=datetime.now, blank=False)

    def __str__(self):
        return self.title