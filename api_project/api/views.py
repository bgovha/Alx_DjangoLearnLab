from rest_framework import generics, viewsets
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

# Keep the existing ListAPIView for backward compatibility
class BookList(generics.ListAPIView):
    """
    API endpoint that allows books to be viewed.
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer

# New ViewSet for full CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    Provides all CRUD operations: list, create, retrieve, update, destroy.
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer

@api_view(['GET'])
def api_overview(request):
    return Response({
        'message': 'Welcome to the Book API!',
        'endpoints': {
            'books': '/api/books/ (coming soon)',
        }
    })

# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
def api_overview(request):
    return Response({
        'message': 'Welcome to the Book API!',
        'endpoints': {
            'books': '/api/books/ (coming soon)',
        }
    })

# Create your views here.

class BookList(generics.ListAPIView):
    """
    API endpoint that allows books to be viewed.
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
