from django.db import models

class Activity(models.Model):
    activity = models.CharField(max_length=30)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.CharField(max_length=30)
    desc = models.TextField(max_length=300)
    # lecturer = models.CharField(max_length=30)
    # link = models.CharField(max_length=250)
    # color = models.CharField(max_length=7)

    def __str__(self):
        return self.activity