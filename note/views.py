from typing import OrderedDict
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoteForm
from .models import NoteModel
from django.contrib.auth.decorators import login_required
import random
from django.http import HttpResponseRedirect,  JsonResponse
from django.template.loader import render_to_string 
from user.models import Profile
from django.contrib.auth.models import User

# Create your views here.

kelas_note = ["rotate-1 yellow-bg", "rotate-1 lazur-bg", "rotate-1 red-bg", "rotate-1 navy-bg",  "rotate-2 lazur-bg", "rotate-2 red-bg", "rotate-2 navy-bg", "rotate-2 yellow-bg"]


@login_required(login_url="/user/login/")
def index(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    notes = NoteModel.objects.filter(user = user)
    
    context = {
        "notes" : notes,
       
        } 
    return render(request, 'note/index.html', context)


@login_required(login_url="/user/login/")
def add_message(request):
    data=dict()
    if request.method == 'POST':
        form = NoteForm(request.POST) 
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            data['form_is_valid'] = True
            notes = NoteModel.objects.all()
            data['note_list'] = render_to_string('note/index2.html',{'notes' :notes})
        else:
            data['form_is_valid'] = False
    else:
        form = NoteForm()

    context = {
		'form': form,
	}
    data['html_form'] = render_to_string('note/note_form.html',context,request=request)
    return JsonResponse(data)

@login_required(login_url="/user/login/")
def delete_message (request,id):
    data = dict()
    note = get_object_or_404(NoteModel,id=id)
    if request.method == "POST":
        note.delete()
        data['form_is_valid'] = True
        notes = NoteModel.objects.all()
        data['note_list'] = render_to_string('note/index2.html',{'notes':notes})
    else:
        context ={'note':note}
        data['html_form'] = render_to_string('note/note_del.html',context,request=request)

    return JsonResponse(data)



    



