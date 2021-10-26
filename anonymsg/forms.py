from django import forms
from .models import AnonymousMessage


class AskForm(forms.ModelForm):
    class Meta:
        model = AnonymousMessage
        fields = (
            "user",
            "anonymous_question",
        )
