from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Post

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

def validate_file_size(f):
    if f.size > MAX_FILE_SIZE:
        raise ValidationError('File too big.')


class PostForm(ModelForm):
    image = forms.ImageField(validators=[validate_file_size])
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']