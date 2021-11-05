from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AnonymousMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    anonymous_question = models.CharField(max_length=200, null=True)
    anonymous_answer = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return self.anonymous_question
