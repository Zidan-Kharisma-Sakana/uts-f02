from django import forms
from django.db.models import fields
from .models import ToDoList

class ToDoListForm(forms.Form):
    class Meta:
        model = ToDoList
        fields = ['title', 'description', 'checklist', 'deadline']
    title_attrs = {
        'type' : 'text',
        'class' : 'input',
        'placeholder' : 'What do you want to do ?',
        'style' : 'width: 100%; padding: 10px 10px; box-sizing: border-box; border-radius: 5px; border : 1px solid #ccc;'
    }
    description_attrs = {
        'type' : 'text',
        'placeholder' : 'insert your description here here',
        'style' : 'width: 100%; padding: 10px 10px; box-sizing: border-box; border-radius: 4px; border : 1px solid #ccc;'
    }

    Title = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs=title_attrs))
    Description = forms.CharField(required=False, max_length=300, widget=forms.Textarea(attrs=description_attrs))