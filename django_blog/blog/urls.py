from django.urls import path
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, 
    PostUpdateView, PostDeleteView, UserPostListView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    TagListView, TagDetailView, TagCreateView, TagUpdateView, TagDeleteView,
    SearchView, AutocompleteView
)

app_name = 'blog'

urlpatterns = [
    # Post URLs
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user_posts'),
    
    # Tag URLs
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tags/create/', TagCreateView.as_view(), name='tag_create'),
    path('tags/<slug:slug>/', TagDetailView.as_view(), name='tag_detail'),
    path('tags/<slug:slug>/update/', TagUpdateView.as_view(), name='tag_update'),
    path('tags/<slug:slug>/delete/', TagDeleteView.as_view(), name='tag_delete'),
    path('tag/<str:tag_slug>/', PostListView.as_view(), name='posts_by_tag'),
    
    # Search URLs
    path('search/', SearchView.as_view(), name='search'),
    path('autocomplete/tags/', AutocompleteView.as_view(), name='autocomplete_tags'),
    
    # Comment URLs (existing)
    path('post/<int:post_pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('post/<int:post_pk>/comment/<int:parent_pk>/reply/', views.add_comment_reply, name='add_comment_reply'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    path('comment/<int:pk>/like/', views.comment_like_toggle, name='comment_like_toggle'),
    path('comments/', views.CommentListView.as_view(), name='comment_list'),
    
    # Tag management
    path('post/<int:pk>/manage-tags/', views.manage_post_tags, name='manage_post_tags'),
]