from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

from .models import *
from crispy_forms.helper import FormHelper

class PhotosUploadForm(forms.ModelForm):
    class Meta: 
        model = MYPhotos
        fields = ('image',)