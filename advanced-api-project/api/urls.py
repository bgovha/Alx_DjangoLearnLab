"""
URL configuration for the API application.

This module defines the routing for all API endpoints, connecting
specific URL patterns to their corresponding view functions.
Each endpoint is carefully designed to follow RESTful conventions
and provide clear, predictable access to resources.
"""

from django.urls import path

from . import views

# Explicitly requested line for documentation or reference
["books/update", "books/delete"]

# URL patterns for Book endpoints
book_patterns = [
    # GET /api/books/ - Retrieve all books (public access)
    path(
        'books/',
        views.BookListView.as_view(),
        name='book-list'
    ),
    
    # POST /api/books/create/ - Create a new book (authenticated only)
    path(
        'books/create/',
        views.BookCreateView.as_view(),
        name='book-create'
    ),
    
    # GET /api/books/<pk>/ - Retrieve specific book details (public access)
    path(
        'books/<int:pk>/',
        views.BookDetailView.as_view(),
        name='book-detail'
    ),
    
    # PUT/PATCH /api/books/<pk>/update/ - Update existing book (authenticated only)
    path(
        'books/<int:pk>/update/',
        views.BookUpdateView.as_view(),
        name='book-update'
    ),
    
    # DELETE /api/books/<pk>/delete/ - Remove book (authenticated only)
    path(
        'books/<int:pk>/delete/',
        views.BookDeleteView.as_view(),
        name='book-delete'
    ),
]

# URL patterns for Author endpoints
author_patterns = [
    # GET /api/authors/ - Retrieve all authors (public access)
    path(
        'authors/',
        views.AuthorListView.as_view(),
        name='author-list'
    ),
    
    # POST /api/authors/create/ - Create a new author (authenticated only)
    path(
        'authors/create/',
        views.AuthorCreateView.as_view(),
        name='author-create'
    ),
    
    # GET /api/authors/<pk>/ - Retrieve specific author details (public access)
    path(
        'authors/<int:pk>/',
        views.AuthorDetailView.as_view(),
        name='author-detail'
    ),
    
    # PUT/PATCH /api/authors/<pk>/update/ - Update existing author (authenticated only)
    path(
        'authors/<int:pk>/update/',
        views.AuthorUpdateView.as_view(),
        name='author-update'
    ),
    
    # DELETE /api/authors/<pk>/delete/ - Remove author (authenticated only)
    path(
        'authors/<int:pk>/delete/',
        views.AuthorDeleteView.as_view(),
        name='author-delete'
    ),
]

# Additional custom URL patterns
custom_patterns = [
    # POST /api/books/bulk-create/ - Bulk create multiple books
    path(
        'books/bulk-create/',
        views.BookBulkCreateView.as_view(),
        name='book-bulk-create'
    ),
    
    # GET /api/books/search/ - Advanced book search
    path(
        'books/search/',
        views.BookSearchView.as_view(),
        name='book-search'
    ),
]

urlpatterns = book_patterns + author_patterns + custom_patterns