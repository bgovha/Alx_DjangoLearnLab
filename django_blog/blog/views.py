from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
)
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.db.models import F, Value, IntegerField
from django.utils import timezone
from .models import Post, Comment, Tag
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm, TagForm, CommentEditForm, CommentSearchForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Post.objects.filter(
            status='published', 
            published_date__lte=timezone.now()
        ).select_related('author').prefetch_related('tags')
        
        # Filter by tag if provided
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__name=tag_slug)
        
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_tags'] = Tag.objects.annotate(
            post_count=Count('posts')
        ).order_by('-post_count')[:10]
        context['search_query'] = self.request.GET.get('q', '')
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related('tags', 'comments__author')
        # Ensure comments are prefetched with their replies and likes
        return Post.objects.select_related('author').prefetch_related(
            'tags', 
            'comments__author', 
            'comments__replies__author',
            'comments__likes'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comment_edit_form'] = CommentEditForm()
        context['similar_posts'] = self.get_similar_posts()
        
        # Organize comments with their replies
        comments = self.object.comments.filter(parent__isnull=True, approved=True)
        context['top_level_comments'] = comments
        
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/includes/comment_form.html'
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        form.instance.author = self.request.user
        form.instance.post = post
        
        # Handle replies
        parent_pk = self.request.POST.get('parent')
        if parent_pk:
            parent_comment = get_object_or_404(Comment, pk=parent_pk)
            form.instance.parent = parent_comment
        
        response = super().form_valid(form)
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'comment_id': self.object.id,
                'message': 'Comment added successfully!'
            })
        
        messages.success(self.request, 'Your comment has been added!')
        return response
    
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors

            }, status=400)
        
        messages.error(self.request, 'There was an error with your comment.')
        return redirect('blog:post_detail', pk=self.kwargs.get('post_pk'))

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentEditForm
    template_name = 'blog/comment_edit.html'
    

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        response = super().form_valid(form)
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'comment_id': self.object.id,
                'content': self.object.content,
                'message': 'Comment updated successfully!'
            })
        
        messages.success(self.request, 'Your comment has been updated!')
        return response
    

    def test_func(self):
        comment = self.get_object()
        return comment.can_edit(self.request.user)
    
    def get_success_url(self):
        return self.object.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()

        return comment.can_delete(self.request.user)
    
    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        post_pk = comment.post.pk
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            comment.delete()
            return JsonResponse({
                'success': True,
                'message': 'Comment deleted successfully!'
            })
        
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('blog:post_detail', pk=post_pk)
    
    def get_success_url(self):
        return self.object.post.get_absolute_url()

@login_required
@require_POST
def comment_like_toggle(request, pk):
    """Toggle like on a comment"""
    comment = get_object_or_404(Comment, pk=pk)
    
    if comment.user_has_liked(request.user):
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'like_count': comment.like_count
    })

class CommentListView(ListView):
    """View to list all comments (for moderation)"""
    model = Comment
    template_name = 'blog/comment_list.html'
    context_object_name = 'comments'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Comment.objects.select_related('author', 'post').prefetch_related('replies', 'likes')
        
        # Filter by search parameters
        search_form = CommentSearchForm(self.request.GET)
        if search_form.is_valid():
            search_query = search_form.cleaned_data.get('search')
            author_query = search_form.cleaned_data.get('author')
            
            if search_query:
                queryset = queryset.filter(content__icontains=search_query)
            if author_query:
                queryset = queryset.filter(author__username__icontains=author_query)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = CommentSearchForm(self.request.GET)
        return context

@login_required
def add_comment_reply(request, post_pk, parent_pk):
    """Handle comment replies"""
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        parent_comment = get_object_or_404(Comment, pk=parent_pk)
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.parent = parent_comment
            comment.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'comment_id': comment.id,
                    'message': 'Reply added successfully!'
                })
            
            messages.success(request, 'Your reply has been added!')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({

                    'success': False,
                    'errors': form.errors
                }, status=400)
            
            messages.error(request, 'There was an error with your reply.')
    
    return redirect('blog:post_detail', pk=post_pk)
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Increment view count
        if self.object.is_published:
            self.object.increment_view_count()
        return response
    
    def get_similar_posts(self):
        post_tags_ids = self.object.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(
            tags__in=post_tags_ids,
            status='published',
            published_date__lte=timezone.now()

        ).exclude(id=self.object.id)
        similar_posts = similar_posts.annotate(
            same_tags=Count('tags')
        ).order_by('-same_tags', '-published_date')[:3]
        return similar_posts

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        context['submit_text'] = 'Create Post'
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Post'
        context['submit_text'] = 'Update Post'
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(
            author=user,
            status='published',
            published_date__lte=timezone.now()
        ).select_related('author').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('blog:post_detail', pk=post.pk)
    
    return redirect('blog:post_detail', pk=post.pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.author or request.user == comment.post.author:
        post_pk = comment.post.pk
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('blog:post_detail', pk=post_pk)
    else:
        messages.error(request, 'You are not authorized to delete this comment.')
        return redirect('blog:post_detail', pk=comment.post.pk)

def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    else:
        posts = Post.objects.all()
    
    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})