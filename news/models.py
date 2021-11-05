from django.contrib.auth.models import User
from django.db import models

class News(models.Model):
    headline = models.CharField(max_length=100)
    body = models.TextField(max_length=1000)
    date = models.DateField(auto_now_add=True)

    is_approved = models.BooleanField(default=False)
