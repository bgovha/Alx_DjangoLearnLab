from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .serializers import (
    PostSerializer, 
    PostCreateUpdateSerializer,
    CommentSerializer
)
User = get_user_model()

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission: 
    - Anyone can read (GET)
    - Only author can edit/delete (PUT, PATCH, DELETE)
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for any request
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        
        # Write permissions only for author
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model.
    Provides: list, create, retrieve, update, partial_update, destroy
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']  # Filter by author ID
    search_fields = ['title', 'content']  # Search in these fields
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']  # Default ordering
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        """Automatically set author to logged-in user"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Custom endpoint: /posts/{id}/comments/
        Returns all comments for a post
        """
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment model.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'author']
    
    def perform_create(self, serializer):
        """Automatically set author to logged-in user"""
        serializer.save(author=self.request.user)
        
class FeedView(generics.ListAPIView):
    """
    "Post.objects.filter(author__in=following_users).order_by"
    GET /api/feed/
    Returns posts from users that the current user follows
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get users that current user follows
        following_users = self.request.user.following.all()
        
        # Get posts from those users, ordered by newest first
        return Post.objects.filter(
            author__in=following_users
        ).order_by('-created_at')
        
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']  # Default: newest first
    
    def get_queryset(self):
        following_users = self.request.user.following.all()
        
        queryset = Post.objects.filter(
            author__in=following_users
        ).select_related('author').prefetch_related(
            'comments',
            'comments__author'
        )
        
        return queryset
    
    #"generics.get_object_or_404(Post, pk=pk)", "Like.objects.get_or_create(user=request.user, post=post)", "Notification.objects.create"]