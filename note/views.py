from django.shortcuts import render, redirect
from .forms import NoteForm
from .models import NoteModel
from django.contrib.auth.decorators import login_required
import random
from django.http import HttpResponseRedirect,  JsonResponse
from django.template.loader import render_to_string 

# Create your views here.

kelas_note = ["rotate-1 yellow-bg", "rotate-1 lazur-bg", "rotate-1 red-bg", "rotate-1 navy-bg",  "rotate-2 lazur-bg", "rotate-2 red-bg", "rotate-2 navy-bg", "rotate-2 yellow-bg"]



def index(request):
    num = random.randint(0, 7)
    kelas_rand = kelas_note[num]
    notes = NoteModel.objects.all()
    context = {
        "notes" : notes,
       
        } 
    return render(request, 'note/index.html', context)

def kelas_rand():
    num = random.randint(0, 7)
    kelas_random = kelas_note[num]
    return kelas_random

def add_message(request):
    data=dict()
    if request.method == 'POST':
        form = NoteForm(request.POST) 
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = NoteForm()

    context = {
		'form': form,
	}
    data['html_form'] = render_to_string('note/note_form.html',context,request=request)
    return JsonResponse(data)


    



