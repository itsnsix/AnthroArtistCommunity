import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.template import Library
from user.models import UserProfile
from thumbnails.fields import ImageField

register = Library()

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

CONTENT_RATINGS = (
    (0, "safe"),
    (1, "questionable"),
    (2, "explicit")
)


def validate_file_size(f):
    if f.size > MAX_FILE_SIZE:
        raise ValidationError('File too big.')


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, unique=False, default='', blank=True, null=True)
    body = models.TextField(max_length=2000, blank=True, unique=False, default='')
    image = ImageField(upload_to='posts/', blank=True, null=True, unique=False, pregenerated_sizes=["small", "large"])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, unique=False)
    content_rating = models.IntegerField(choices=CONTENT_RATINGS, default=0, unique=False, null=False,
                                      blank=False)
    tags = models.CharField(max_length=300, unique=False, blank=True, default='')

    def get_author_profile(self):
        return UserProfile.objects.get(user_id=self.author.id)

    def get_author_display_name(self):
        if self.get_author_profile().display_name:
            return self.get_author_profile().display_name
        else:
            return self.author.username

    def get_author_icon_avatar(self):
        return self.get_author_profile().get_icon_avatar()

    def get_child_count(self):
        return Post.objects.filter(parent_id=self.id).count()

    def get_short_body(self):
        if len(self.body) > 200:
            return self.body[0:197] + '...'
        else:
            return self.body

    def get_body_length(self):
        return len(self.body)

    def get_url(self):
        return '/post/' + str(self.id)

    def get_tag_count(self):
        return Tag.objects.filter(posts=self).count()

    def get_tags(self):
        return ', '.join(Tag.objects.values_list('tag_name', flat=True).filter(posts=self))


class Tag(models.Model):
    tag_name = models.CharField(max_length=128, unique=True, blank=False, null=False)
    posts = models.ManyToManyField(Post)


@register.inclusion_tag("post/post-form.html")
def new_post_form(form, parent=None):
    return {'form': form, 'parent': parent}
