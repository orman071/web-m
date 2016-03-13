from django import forms
from django.contrib.auth.models import User

from .models import Question, Answer


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "text"]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["text", "question"]


class UserCreationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def save(self):
        user = User.objects.create_user(**self.cleaned_data)
        return user
