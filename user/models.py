import datetime

from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

import string, secrets


def generate_invite_code():
    return ''.join(
        secrets.choice(
            string.ascii_letters
            + string.digits +
            string.punctuation)
        for _ in range(24))


# Create your models here.
class Invite(models.Model):
    invitee = models.ForeignKey(User, related_name='invitee', null=True, blank=True, on_delete=models.SET_NULL)
    inviter = models.ForeignKey(User, related_name='inviter', null=True, on_delete=models.SET_NULL)
    invite_code = models.CharField(null=False, unique=True, default=generate_invite_code)


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, unique=True, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=32, unique=False, blank=True, null=False, default='')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, unique=False, default=None)
    about = models.TextField(max_length=250, blank=True, null=True, unique=False, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return '/static/images/default_pfp.png'

    def get_display_name(self):
        if self.display_name:
            return self.display_name
        else:
            return self.user.username