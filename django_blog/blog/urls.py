from django.urls import path
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, 
    PostUpdateView, PostDeleteView, UserPostListView,
    CommentCreateView, CommentUpdateView, CommentDeleteView, CommentListView
)

app_name = 'blog'

urlpatterns = [
    # Post URLs (existing)
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user_posts'),
    path('tag/<str:tag_slug>/', PostListView.as_view(), name='posts_by_tag'),
    
    # Comment URLs
    path('post/<int:post_pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('post/<int:post_pk>/comment/<int:parent_pk>/reply/', views.add_comment_reply, name='add_comment_reply'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    path('comment/<int:pk>/like/', views.comment_like_toggle, name='comment_like_toggle'),
    path('comments/', CommentListView.as_view(), name='comment_list'),
]