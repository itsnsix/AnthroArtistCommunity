import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from user.models import UserProfile


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, unique=False, default='Untitled')
    body = models.TextField(max_length=2000, blank=True, unique=False, default='')
    image = models.ImageField(upload_to='posts/', blank=True, null=True, unique=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_author_profile(self):
        return UserProfile.objects.get(user_id=self.author.id)

