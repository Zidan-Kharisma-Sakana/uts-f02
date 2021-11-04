from django import forms
from django.forms import fields
from django.forms.widgets import Input, Textarea
from .models import NoteModel


class NoteForm(forms.ModelForm):
	timestamp = forms.DateInput()
	class Meta:
		model = NoteModel
		fields = ('title','timestamp','message')

		

		widgets = {
			'title': forms.TextInput(
				attrs = {
					'class':'form-control',
					'placeholder':'max 13 character',}
				),
			'timestamp': forms.DateInput(
				attrs = {
					'class':'form-control',
					'type' : 'date'
					}
				),

			'message': forms.Textarea(
				attrs = {
					'class':'form-control',}
				),

		}