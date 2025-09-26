from django.shortcuts import render

# Create your views here.
"""
API views for handling Author and Book resources.
"""

from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, AuthorDetailSerializer

class AuthorListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating authors.
    
    Supports:
    - GET: Retrieve list of all authors (without nested books for performance)
    - POST: Create a new author
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    def get_serializer_context(self):
        """Add context to control nested serialization."""
        context = super().get_serializer_context()
        context['include_books'] = False  # Don't include books in list view for performance
        return context

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting specific authors.
    
    Supports:
    - GET: Retrieve detailed author information with nested books
    - PUT/PATCH: Update author information
    - DELETE: Remove an author
    """
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer  # Use detailed serializer with books

class BookListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating books.
    
    Supports:
    - GET: Retrieve list of all books
    - POST: Create a new book with validation
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting specific books.
    
    Supports:
    - GET: Retrieve detailed book information
    - PUT/PATCH: Update book information
    - DELETE: Remove a book
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer