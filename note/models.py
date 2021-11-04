from django.db import models
import random

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

kelas_note = ["rotate-1 yellow-bg", "rotate-1 lazur-bg", "rotate-1 red-bg", "rotate-1 navy-bg",  "rotate-2 lazur-bg", "rotate-2 red-bg", "rotate-2 navy-bg", "rotate-2 yellow-bg"]

def kelas_rand():
    num = random.randint(0, 7)
    kelas_random = kelas_note[num]
    return kelas_random
    
class NoteModel(models.Model):
    kelas = models.kelasrand
    title = models.CharField(max_length=13)
    timestamp = models.DateField(null=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.user.username} | {self.title}"
