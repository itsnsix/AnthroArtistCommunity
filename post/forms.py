from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm\

from .models import Post

class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'image']


    def __init__(self, *args, **kwargs):
        hide_title = kwargs.pop('hide_title', False)
        super(PostForm, self).__init__(*args, **kwargs)
        if hide_title:
            self.fields['title'].widget = forms.HiddenInput()


    def is_valid(self):
        f = self.save(commit=False)
        if not f.body and not f.image:
            print('here')
            self.add_error('body', ValidationError('Post cannot be blank.'))
            return False
        return True