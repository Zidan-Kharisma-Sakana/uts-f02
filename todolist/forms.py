from django import forms
# from .models import ToDoList

class ToDoListForm(forms.Form):
    position = forms.CharField()
    # class Meta:
    #     model = ToDoList
    #     fields = (
    #         "user", "text",
    #     )