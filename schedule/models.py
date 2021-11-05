from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    activity = models.CharField(max_length=30)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.CharField(max_length=30)
    desc = models.TextField(max_length=300)

    def __str__(self):
        return self.activity