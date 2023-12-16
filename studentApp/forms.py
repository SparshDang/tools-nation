
from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput
from ckeditor.widgets import CKEditorWidget

from studentApp.models import Notepad, Reminder, FileUploads

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")
        widgets = {'password': PasswordInput()}

    def clean(self):
        pass

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ( "first_name", "last_name","username", "password", "email",)
        widgets = {'password': PasswordInput()}


class NotepadForm(forms.ModelForm):
    class Meta:
        model = Notepad
        fields = ("body",)
        widgets = {
            'body':CKEditorWidget()
        }

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ('schedule', "text")
        widgets = {
            'schedule' : forms.TextInput(attrs={'type':'datetime-local'})
        }

class FileForms(forms.Form):
    file = forms.FileField(max_length=200)