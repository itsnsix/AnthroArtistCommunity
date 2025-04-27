from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.index, name="post_index"),
    path('posts/<int:page>', views.index, name="post_index"),
    path('post/<int:post_id>', views.show, name="show_post"),
    path('post/new', views.new, name="new_post"),
    path('post/<int:post_id>/edit', views.edit, name="edit_post"),
    path('post/<int:post_id>/delete', views.delete, name="delete_post")
]
