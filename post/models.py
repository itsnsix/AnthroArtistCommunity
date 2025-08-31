import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from user.models import UserProfile

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

def validate_file_size(f):
    if f.size > MAX_FILE_SIZE:
        raise ValidationError('File too big.')

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, unique=False, default='Untitled')
    body = models.TextField(max_length=2000, blank=True, unique=False, default='')
    image = models.ImageField(upload_to='posts/', blank=True, null=True, unique=False, validators=[])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, unique=False)

    def get_author_profile(self):
        return UserProfile.objects.get(user_id=self.author.id)

    def get_child_count(self):
        return Post.objects.filter(parent_id=self.id).count()

