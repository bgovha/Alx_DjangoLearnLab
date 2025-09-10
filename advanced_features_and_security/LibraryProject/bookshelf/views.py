from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Article
from .forms import ArticleForm

@login_required
@permission_required('book_list.can_view', raise_exception=True)
def article_list(request):
    articles = Article.objects.all()
    if not request.user.has_perm('book_list.can_publish'):
        articles = articles.filter(is_published=True) | articles.filter(author=request.user)
    return render(request, 'articles/list.html', {'articles': articles})

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if not article.is_published and not request.user.has_perm('bookshelf.can_publish'):
        return HttpResponseForbidden("You don't have permission to view unpublished articles.")
    return render(request, 'articles/detail.html', {'article': article})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Article created successfully!')
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'articles/form.html', {'form': form, 'title': 'Create Article'})

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # Additional check: users can only edit their own articles unless they have publish permission
    if article.author != request.user and not request.user.has_perm('bookshelf.can_publish'):
        return HttpResponseForbidden("You can only edit your own articles.")
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/form.html', {'form': form, 'title': 'Edit Article'})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # Additional check: users can only delete their own articles unless they have publish permission
    if article.author != request.user and not request.user.has_perm('bookshelf.can_publish'):
        return HttpResponseForbidden("You can only delete your own articles.")
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted successfully!')
        return redirect('article_list')
    return render(request, 'articles/confirm_delete.html', {'article': article})

@login_required
@permission_required('bookshelf.can_publish', raise_exception=True)
def article_publish(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.is_published = True
    article.save()
    messages.success(request, 'Article published successfully!')
    return redirect('article_detail', pk=article.pk)
