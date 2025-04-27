from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Invite, UserProfile

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB


def validate_invite_code(invite_code):
    try:
        invitation = Invite.objects.get(invite_code=invite_code)
        if invitation.invitee:
            raise ValidationError('This invite code has already been used.')
    except Invite.DoesNotExist:
        raise ValidationError('Invalid invite code.')


def validate_file_size(f):
    if f.size > MAX_FILE_SIZE:
        raise ValidationError('File too big.')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class InviteForm(forms.Form):
    invite_code = forms.CharField(
        validators=[validate_invite_code]
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserProfileForm(ModelForm):
    avatar = forms.ImageField(validators=[validate_file_size])

    class Meta:
        model = UserProfile
        fields = ['avatar', 'about']
