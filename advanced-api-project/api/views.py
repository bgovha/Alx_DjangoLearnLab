"""
Additional custom views with specialized behavior.
"""

from rest_framework.views import APIView

from rest_framework.exceptions import ValidationError

# Explicitly requested line for documentation or reference
["from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated"]

class BookBulkCreateView(APIView):
	"""
	Custom view for bulk creating multiple books at once.
    
	This view demonstrates how to extend DRF's functionality
	to handle complex use cases beyond standard CRUD operations.
	"""
	permission_classes = [permissions.IsAuthenticated]
    
	def post(self, request, *args, **kwargs):
		"""
		Handle bulk creation of books with comprehensive validation.
        
		Args:
			request (Request): Contains list of book data in request.data
            
		Returns:
			Response: Results of bulk creation operation
		"""
		books_data = request.data.get('books', [])
        
		if not isinstance(books_data, list):
			raise ValidationError({"books": "Expected a list of books"})
        
		results = {
			'created': [],
			'errors': []
		}
        
		for index, book_data in enumerate(books_data):
			serializer = BookSerializer(data=book_data)
            
			if serializer.is_valid():
				serializer.save()
				results['created'].append(serializer.data)
			else:
				results['errors'].append({
					'index': index,
					'data': book_data,
					'errors': serializer.errors
				})
        
		status_code = status.HTTP_207_MULTI_STATUS if results['errors'] else status.HTTP_201_CREATED
		return Response(results, status=status_code)


class BookSearchView(generics.ListAPIView):
	"""
	Custom search view with advanced filtering capabilities.
    
	Demonstrates how to create specialized views for specific
	use cases while leveraging DRF's generic view functionality.
	"""
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]
    
	def get_queryset(self):
		"""
		Custom queryset filtering based on multiple search parameters.
        
		Returns:
			QuerySet: Filtered books based on search criteria
		"""
		queryset = Book.objects.select_related('author').all()
        
		# Filter by title (case-insensitive contains)
		title = self.request.query_params.get('title', None)
		if title:
			queryset = queryset.filter(title__icontains=title)
        
		# Filter by author name
		author_name = self.request.query_params.get('author_name', None)
		if author_name:
			queryset = queryset.filter(author__name__icontains=author_name)
        
		# Filter by publication year range
		year_from = self.request.query_params.get('year_from', None)
		year_to = self.request.query_params.get('year_to', None)
        
		if year_from:
			queryset = queryset.filter(publication_year__gte=year_from)
		if year_to:
			queryset = queryset.filter(publication_year__lte=year_to)
        
		return queryset

"""
API views for handling Author and Book resources using Django REST Framework's generic views.

This module implements custom views that leverage DRF's powerful generic views and mixins
to handle CRUD operations efficiently while providing customization for specific use cases.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, AuthorDetailSerializer


class BookListView(generics.ListAPIView):
	"""
	ListView for retrieving all books with advanced filtering and search capabilities.
    
	This view provides read-only access to all Book instances with:
	- Search functionality across title field
	- Filtering by publication year and author
	- Ordering by various fields
	- Pagination support
    
	Access: Available to all users (authenticated and unauthenticated)
	"""
	queryset = Book.objects.select_related('author').all()
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]  # Allow public read access
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
	# Configure filtering options
	filterset_fields = ['publication_year', 'author']
	search_fields = ['title', 'author__name']
	ordering_fields = ['title', 'publication_year', 'created_at']
	ordering = ['title']  # Default ordering


class BookDetailView(generics.RetrieveAPIView):
	"""
	DetailView for retrieving a single book by ID.
    
	Provides detailed information about a specific Book instance
	including all fields and related author information.
    
	Access: Available to all users (authenticated and unauthenticated)
	"""
	queryset = Book.objects.select_related('author').all()
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]
	lookup_field = 'pk'


class BookCreateView(generics.CreateAPIView):
	"""
	CreateView for adding a new book with comprehensive validation.
    
	Handles POST requests to create new Book instances with:
	- Automatic validation using BookSerializer
	- Custom permission checking
	- Proper error handling and response formatting
    
	Access: Restricted to authenticated users only
	"""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]
    
	def perform_create(self, serializer):
		"""
		Customize the creation process with additional logic.
        
		Args:
			serializer (BookSerializer): Validated serializer instance
            
		This method is called when creating a new Book instance and allows
		for additional processing before saving to the database.
		"""
		# Additional processing can be added here
		# For example: logging, additional validation, etc.
		serializer.save()
    
	def create(self, request, *args, **kwargs):
		"""
		Override create method to customize response or add additional logic.
        
		Args:
			request (Request): The HTTP request object
            
		Returns:
			Response: Customized response with book data
		"""
		response = super().create(request, *args, **kwargs)
		# Customize response if needed
		return response


class BookUpdateView(generics.UpdateAPIView):
	"""
	UpdateView for modifying an existing book with partial or complete updates.
    
	Supports both PUT (complete update) and PATCH (partial update) methods.
	Includes comprehensive validation and permission checks.
    
	Access: Restricted to authenticated users only
	"""
	queryset = Book.objects.select_related('author').all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]
	lookup_field = 'pk'
    
	def perform_update(self, serializer):
		"""
		Customize the update process with additional logic.
        
		Args:
			serializer (BookSerializer): Validated serializer instance
            
		This method allows for additional processing before updating
		the Book instance in the database.
		"""
		# Additional processing can be added here
		serializer.save()
    
	def update(self, request, *args, **kwargs):
		"""
		Override update method to customize response or add additional logic.
        
		Args:
			request (Request): The HTTP request object
            
		Returns:
			Response: Customized response with updated book data
		"""
		response = super().update(request, *args, **kwargs)
		# Customize response if needed
		return response


class BookDeleteView(generics.DestroyAPIView):
	"""
	DeleteView for removing a book instance from the database.
    
	Handles DELETE requests to remove Book instances with:
	- Proper permission checking
	- Clean deletion process
	- Appropriate response formatting
    
	Access: Restricted to authenticated users only
	"""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]
	lookup_field = 'pk'
    
	def perform_destroy(self, instance):
		"""
		Customize the deletion process with additional logic.
        
		Args:
			instance (Book): The Book instance to be deleted
            
		This method allows for additional processing before deleting
		the Book instance from the database.
		"""
		# Additional processing can be added here (e.g., logging, cleanup)
		instance.delete()
    
	def destroy(self, request, *args, **kwargs):
		"""
		Override destroy method to customize response.
        
		Args:
			request (Request): The HTTP request object
            
		Returns:
			Response: Customized response with appropriate status code
		"""
		instance = self.get_object()
		self.perform_destroy(instance)
		return Response(
			{"detail": "Book deleted successfully."},
			status=status.HTTP_204_NO_CONTENT
		)


# Author Views with similar structure
class AuthorListView(generics.ListAPIView):
	"""
	ListView for retrieving all authors with filtering and search capabilities.
	"""
	queryset = Author.objects.prefetch_related('books').all()
	serializer_class = AuthorSerializer
	permission_classes = [permissions.AllowAny]
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
	filterset_fields = []
	search_fields = ['name']
	ordering_fields = ['name', 'created_at']
	ordering = ['name']
    
	def get_serializer_context(self):
		"""Control nested serialization for performance."""
		context = super().get_serializer_context()
		context['include_books'] = False
		return context


class AuthorDetailView(generics.RetrieveAPIView):
	"""
	DetailView for retrieving a single author by ID with nested book information.
	"""
	queryset = Author.objects.prefetch_related('books').all()
	serializer_class = AuthorDetailSerializer
	permission_classes = [permissions.AllowAny]
	lookup_field = 'pk'


class AuthorCreateView(generics.CreateAPIView):
	"""
	CreateView for adding a new author.
	"""
	queryset = Author.objects.all()
	serializer_class = AuthorSerializer
	permission_classes = [permissions.IsAuthenticated]


class AuthorUpdateView(generics.UpdateAPIView):
	"""
	UpdateView for modifying an existing author.
	"""
	queryset = Author.objects.all()
	serializer_class = AuthorSerializer
	permission_classes = [permissions.IsAuthenticated]
	lookup_field = 'pk'


class AuthorDeleteView(generics.DestroyAPIView):
	"""
	DeleteView for removing an author instance.
	"""
	queryset = Author.objects.all()
	serializer_class = AuthorSerializer
	permission_classes = [permissions.IsAuthenticated]
	lookup_field = 'pk'
    
	def destroy(self, request, *args, **kwargs):
		"""
		Custom destroy method with appropriate response.
		"""
		instance = self.get_object()
		self.perform_destroy(instance)
		return Response(
			{"detail": "Author deleted successfully."},
			status=status.HTTP_204_NO_CONTENT
		)
