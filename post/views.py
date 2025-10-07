from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render, redirect

from post.forms import PostForm
from post.models import Post, Tag
from user.models import UserProfile


# Create your views here.
def index(request, page=1):
    posts = Post.objects.filter(parent_id=None).order_by('-created_at')
    paginator = Paginator(posts, 10)
    paginated_posts = paginator.get_page(page)
    return render(request, 'post/index.html', {'paginated_posts': paginated_posts})


def show(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound('Post not found.')

    if post.parent_id:
        post = Post.objects.get(pk=post.parent_id)

    comments = Post.objects.filter(parent_id=post.id)
    form = PostForm(hide_title=True, hide_tags=True)
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user_id=request.user.id)
    else:
        user_profile = None
    return render(request, 'post/show.html', {'post': post, 'form': form, 'comments': comments})


@login_required
def new(request, parent_id=None):
    # GET: Render the new post form
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'post/new.html', {'form': form})

    # POST: Process the new post
    if request.method == 'POST':
        # Turn the user data into a PostForm object
        form = PostForm(request.POST, request.FILES, hide_title=True)

        # check the form is valid
        if form.is_valid():

            # turn the form into a Post object
            post = form.save(commit=False)

            # Check if this post is a comment (will have a parent_id)
            if parent_id:
                try:
                    # If the parent exists, relate them
                    parent = Post.objects.get(pk=parent_id)
                    post.parent = parent
                except Post.DoesNotExist:
                    # If the parent doesn't exist, they shouldn't be abel to reply
                    return HttpResponseNotFound('Thread does not exist.')


            # Set the post author
            post.author = request.user

            # Save the new post
            post.save()

            # Parse tags
            for tag_name in post.tags.split(' '):
                if Tag.objects.filter(tag_name=tag_name.replace('_', ' ')).exists():
                    t = Tag.objects.filter(tag_name=tag_name.replace('_', ' ')).first()
                else:
                    t = Tag.objects.create(tag_name=tag_name.replace('_', ' '))

                t.posts.add(post)

            # If the post was a comment, go to the parent thread
            if parent_id:
                return redirect('show_post', post_id=parent_id)
            else:
                #else go to the new thread
                return redirect('show_post', post_id=post.id)
        else:
            # If the post was an invalid comment, go to the parent thread
            if parent_id:
                return render(request, f'post/show.html', {'post': Post.objects.get(pk=parent_id), 'form': form, 'comments': Post.objects.filter(parent_id=parent_id)})
            else:
                # Else go back to the new post page.
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
