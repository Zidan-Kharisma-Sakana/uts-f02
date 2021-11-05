from django import forms
from .models import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('headline', 'body')
        labels = {
            'headline' : '',
            'body' : ''
        }
        widgets = {
            'headline' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Headline/Title'}),
            'body' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Body'})
        }