from django.urls import path
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, 
    PostUpdateView, PostDeleteView, UserPostListView
)

app_name = 'blog'

urlpatterns = [
    # Post CRUD URLs
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    # User-specific posts
    path('user/<str:username>/', UserPostListView.as_view(), name='user_posts'),
    
    # Comment URLs
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    
    # Tag URLs
    path('tag/<str:tag_slug>/', PostListView.as_view(), name='posts_by_tag'),
]