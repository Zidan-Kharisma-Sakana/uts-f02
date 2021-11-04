from django import forms
from django.forms import fields
from django.forms.widgets import Textarea
from .models import NoteModel


class NoteForm(forms.ModelForm):
	timestamp = forms.DateTimeInput()
	class Meta:
		model = NoteModel
		fields = ('title','timestamp','message')
	