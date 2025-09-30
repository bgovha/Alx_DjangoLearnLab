"""
URL configuration for the API application.

This module defines the routing for all API endpoints, connecting
specific URL patterns to their corresponding view functions.
Each endpoint is carefully designed to follow RESTful conventions
and provide clear, predictable access to resources.
"""
"""
Enhanced URL configuration with advanced filtering, searching, and ordering endpoints.

This module provides comprehensive API endpoints for accessing book data
with powerful query capabilities.
"""

from django.urls import path
from . import views

# Enhanced URL patterns for Book endpoints with advanced query capabilities
book_patterns = [
    # GET /api/books/ - Retrieve all books with advanced filtering, searching, and ordering
    path(
        'books/',
        views.BookListView.as_view(),
        name='book-list'
    ),
    
    # GET /api/books/advanced-search/ - Advanced universal search
    path(
        'books/advanced-search/',
        views.BookAdvancedSearchView.as_view(),
        name='book-advanced-search'
    ),
    
    # GET /api/books/filter-options/ - Discover available filter options
    path(
        'books/filter-options/',
        views.BookFilterOptionsView.as_view(),
        name='book-filter-options'
    ),
    
    # POST /api/books/create/ - Create a new book (authenticated only)
    path(
        'books/create/',
        views.BookCreateView.as_view(),
        name='book-create'
    ),
    
    # GET /api/books/<pk>/ - Retrieve specific book details
    path(
        'books/<int:pk>/',
        views.BookDetailView.as_view(),
        name='book-detail'
    ),
    
    # PUT/PATCH /api/books/<pk>/update/ - Update existing book
    path(
        'books/<int:pk>/update/',
        views.BookUpdateView.as_view(),
        name='book-update'
    ),
    
    # DELETE /api/books/<pk>/delete/ - Remove book
    path(
        'books/<int:pk>/delete/',
        views.BookDeleteView.as_view(),
        name='book-delete'
    ),
]

# Author endpoints (keeping existing structure)
author_patterns = [
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
]

urlpatterns = book_patterns + author_patterns