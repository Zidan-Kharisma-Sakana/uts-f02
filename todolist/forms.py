from django import forms

class ToDoListForm(forms.Form):
    class Meta:
        todolist = forms.CharField()
    title_attrs = {
        'type' : 'text',
        'placeholder' : 'What do you want to do ?'
    }