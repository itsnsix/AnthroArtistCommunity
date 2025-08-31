from django.shortcuts import render

from post.models import Post


# Create your views here.
def home(request):
    posts = Post.objects.filter(parent_id=None).order_by('-created_at')[0:5]
    return render(request, 'home/home.html', {'posts': posts})