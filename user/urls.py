from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('invite/', views.invite, name='invite'),
    path('register/', views.sign_up, name='register'),
    path('users/', views.user_index, name='user_index'),
    path('users/<int:page>', views.user_index, name='user_index'),
    path('profile/<int:user_id>', views.show_profile, name='profile'),
    path('profile/<int:user_id>/edit', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name='change_password')
]
