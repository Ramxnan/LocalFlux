from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from .models import File

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    college_code = forms.CharField(max_length=6, required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'college_code']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email
    
    def clean_college_code(self):
        code = self.cleaned_data.get('college_code')
        if code != '560035':
            raise forms.ValidationError("Invalid college code. Please contact system admin for further instructions.")
        return code

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Set email as username
        if commit:
            user.save()
        return user



class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=PasswordInput())


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file']