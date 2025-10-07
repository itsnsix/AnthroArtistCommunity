import re
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'tags', 'content_rating']

    def __init__(self, *args, **kwargs):
        hide_title = kwargs.pop('hide_title', False)
        hide_tags = kwargs.pop('hide_tags', False)
        super(PostForm, self).__init__(*args, **kwargs)
        if hide_title:
            self.fields['title'].widget = forms.HiddenInput()
        if hide_tags:
            self.fields['tags'].widget = forms.HiddenInput()

    def is_valid(self):
        try:
            f = self.save(commit=False)
        except ValueError:
            return False
        if not f.body and not f.image:
            self.add_error('body', ValidationError('Post cannot be blank.'))
            return False

        tag_search = re.search(r'[^A-Za-z0-9_\-() ]', f.tags)
        if tag_search:
            self.add_error('tags', ValidationError(f'Invalid tag character: {tag_search[0]}'))
            return False

        return True
