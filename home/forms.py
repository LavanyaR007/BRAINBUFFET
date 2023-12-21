from django import forms
from .models import FAQ


class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = [ 'question']