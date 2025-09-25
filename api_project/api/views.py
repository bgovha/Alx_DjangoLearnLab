
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

# Keep the existing ListAPIView but add permissions
class BookList(generics.ListAPIView):
    """
    API endpoint that allows books to be viewed.
    Now requires authentication to access.
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

# ViewSet with different permission levels
class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    Provides all CRUD operations: list, create, retrieve, update, destroy.
    
    Permissions:
    - Read operations: Any authenticated user
    - Write operations: Admin users only
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            # Allow any authenticated user to view books
            permission_classes = [IsAuthenticated]
        else:
            # Only admin users can create, update, or delete books
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

# Public view for book listing (no authentication required)
class PublicBookList(generics.ListAPIView):
    """
    Public API endpoint that allows anyone to view books.
    No authentication required.
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # No authentication required

@api_view(['GET'])
def api_overview(request):
    return Response({
        'message': 'Welcome to the Book API!',
        'endpoints': {
            'books': '/api/books/ (coming soon)',
        }
    })
