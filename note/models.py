from django.db import models
from django.db import models
from django.contrib.auth.models import User
from user.models import Profile

# Create your models here.    
class NoteModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=13)
    timestamp = models.DateField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f" {self.title}"
