from django.shortcuts import render, redirect


from .models import note
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    notes = note.objects.all()
    return render(request, template_name="note/index.html")