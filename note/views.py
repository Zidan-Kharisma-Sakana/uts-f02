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
    notes = NoteModel.objects.all()
    data = {"list_note" : notes} 
    print('asas')
    return render(request, 'note/index.html', context=data)

def add_message(request):
    num = random.randint(0, 7)
    kelas_rand = kelas_note[num]
    form = NoteForm() 
    print('asas')
    context = {
		'form': form,
	}
    html_form = render_to_string('note/note_form.html',context,request=request)
    print('asas')

    return JsonResponse({'html_form':html_form})


    



