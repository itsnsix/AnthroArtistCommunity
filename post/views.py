from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render, redirect

from post.forms import PostForm
from post.models import Post


# Create your views here.
def index(request, page=1):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    paginated_posts = paginator.get_page(page)
    return render(request, 'post/index.html', {'paginated_posts': paginated_posts})


def show(request, post_id):
    post = Post.objects.filter(pk=post_id)
    if not post.exists():
        return HttpResponseNotFound('Post not found.')

    post = post.first()
    return render(request, 'post/show.html', {'post': post})


@login_required
def new(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'post/new.html', {'form': form})

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('show_post', post_id=post.id)
        else:
            return render(request, 'post/new.html', {'form': form})

@login_required
def edit(request, post_id):

    post = Post.objects.filter(pk=post_id)
    if not post.exists():
        return HttpResponseNotFound('Post not found.')

    post = post.first()

    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'post/edit.html', {'form': form})

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=Post.objects.get(pk=post_id))
        if form.is_valid():
            post = form.save()
            return redirect('show_post', post_id=post.id)
        else:
            return render(request, 'post/edit.html', {'form': form})

@login_required
def delete(request, post_id):

    post = Post.objects.filter(pk=post_id)
    if not post.exists():
        return HttpResponseNotFound('Post not found.')

    post = post.first()

    if post.author != request.user:
        return HttpResponseForbidden('You do not have permission to delete this post.')

    if request.method == 'GET':
        return render(request, 'post/delete.html', {'post': post})

    if request.method == 'DELETE':
        post.delete()
        return redirect('post_index')
