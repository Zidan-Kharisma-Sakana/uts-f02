from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = ['user']

    activity_attrs = {
        'type':'text',
        'class':'input'
    }

    date_atrrs = {
        'type':'hidden',
    }

    time_attrs = {
        'type':'time',
        'format':'%H:%M',
    }

    type_choices = [
        ('general', 'General'),
        ('course', 'Course'),
        ('appointment', 'Appointment'),
        ('hobby', 'Hobby')
    ]

    desc_attrs = {
        'class':'input'
    }

    activity = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs=activity_attrs), error_messages={'required':'Enter Activity Title'})
    year = forms.IntegerField(required=False, widget=forms.NumberInput(attrs=date_atrrs))
    month = forms.IntegerField(required=False, widget=forms.NumberInput(attrs=date_atrrs))
    day = forms.IntegerField(required=False, widget=forms.NumberInput(attrs=date_atrrs))
    start_time = forms.TimeField(required=True, widget=forms.TimeInput(attrs=time_attrs), error_messages={'required':'Enter Start Time'})
    end_time = forms.TimeField(required=True, widget=forms.TimeInput(attrs=time_attrs), error_messages={'required':'Enter End Time'})
    type = forms.CharField(required=True, max_length=30, widget=forms.Select(choices=type_choices), error_messages={'required':'Choose Type'})
    desc = forms.CharField(required=False, max_length=300, widget=forms.Textarea(attrs=desc_attrs))