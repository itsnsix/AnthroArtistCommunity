from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.core.signing import BadSignature
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash

from post.models import Post
from .forms import LoginForm, RegisterForm, InviteForm, UserProfileForm
from .models import Invite, UserProfile


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('/')

        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'user/login.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('login')


def invite(request):

    if request.method == 'GET':
        form = InviteForm()
        return render(request, 'user/invite.html', {'form': form})

    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            invite_code = form.cleaned_data['invite_code']

            response = redirect('register')
            response.set_signed_cookie('invite_code', invite_code)
            return response
        else:
            return render(request, 'user/invite.html', {'form': form})


def sign_up(request):
    if request.method == 'GET':
        try:
            request.get_signed_cookie('invite_code')
            form = RegisterForm()
            return render(request, 'user/register.html', {'invited': True, 'form': form})
        except (KeyError, BadSignature):
            return render(request, 'user/register.html', {'invited': False})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            invite_code = request.get_signed_cookie('invite_code')
            invitation = Invite.objects.get(invite_code=invite_code)
            invitation.invitee = user
            invitation.save()

            profile = UserProfile(user=user)
            profile.save()

            messages.success(request, 'You have singed up successfully.')
            response = redirect('login')
            response.delete_cookie('invite_code')
            return response
        else:
            return render(request, 'user/register.html', {'form': form})


def show_profile(request, user_id):
    try:
        profile = UserProfile.objects.get(user_id=user_id)
        posts = Post.objects.filter(author_id=user_id).order_by('-created_at')[0:5]
        return render(request, 'user/show.html', {'profile': profile, 'posts': posts})

    except UserProfile.DoesNotExist:
        return HttpResponseNotFound('User Not Found')


def edit_profile(request, user_id):
    if request.method == 'GET':
        if request.user.id == user_id:
            form = UserProfileForm(instance=UserProfile.objects.get(user_id=user_id))
            return render(request, 'user/edit.html', {'form': form})
        else:
            return HttpResponseForbidden('Forbidden')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=UserProfile.objects.get(user_id=user_id))
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user_id)
        else:
            return render(request, 'user/edit.html', {'form': form})


def user_index(request, page=1):
    profiles = UserProfile.objects.all().order_by('id')
    paginator = Paginator(profiles, 10)
    paginated_profiles = paginator.get_page(page)
    return render(request, 'user/index.html', {'paginated_profiles': paginated_profiles})

@login_required
def change_password(request):
    if request.method == 'GET':
        form = PasswordChangeForm(request.user)
        return render(request, 'user/change_password.html', {'form': form})

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'user/change_password.html', {'form': form})