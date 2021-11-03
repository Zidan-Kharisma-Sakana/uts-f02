from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=200)
    checklist = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    createTodo = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        order_with_respect_to = 'user'