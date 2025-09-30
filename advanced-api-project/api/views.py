"""
Enhanced API views with comprehensive filtering, searching, and ordering capabilities.

This module implements advanced query features for the Book model API,
providing users with powerful tools to access and manipulate data efficiently.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, AuthorDetailSerializer
from .filters import BookFilter, AdvancedBookSearchFilter


class BookListView(generics.ListAPIView):
	"""
	Enhanced ListView for retrieving books with advanced filtering, searching, and ordering.
    
	This view provides comprehensive query capabilities:
    
	FILTERING:
	- Exact field matching: title, author, publication_year
	- Partial matching: title_contains, author_name
	- Range filtering: publication_year_min, publication_year_max, publication_year_range
	- Combined filtering: title_or_author
    
	SEARCHING:
	- Text search across title and author name fields
	- Case-insensitive partial matching
    
	ORDERING:
	- Order by any book field: title, publication_year, created_at, updated_at
	- Multiple field ordering support
	- Default ordering by title
    
	Example queries:
	GET /api/books/?title_contains=harry&publication_year_min=2000
	GET /api/books/?search=rowling&ordering=-publication_year,title
	GET /api/books/?title_or_author=potter&publication_year_range_min=1990&publication_year_range_max=2000
	"""
    
	queryset = Book.objects.select_related('author').all()
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]
    
	# Configure filter backends for advanced query capabilities
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
	# DjangoFilterBackend configuration
	filterset_class = BookFilter
    
	# SearchFilter configuration
	search_fields = [
		'title',           # Exact search on title
		'author__name',    # Search in author name
		'=publication_year',  # Exact match for publication year
	]
    
	# OrderingFilter configuration
	ordering_fields = [
		'title',
		'publication_year',
		'created_at',
		'updated_at',
		'author__name',  # Order by author name
	]
	ordering = ['title']  # Default ordering
    
	def get_queryset(self):
		"""
		Enhance the base queryset with additional optimizations and custom filtering.
        
		Returns:
			QuerySet: Optimized and potentially pre-filtered queryset
		"""
		queryset = super().get_queryset()
        
		# Additional custom filtering logic can be added here
		# For example, based on user permissions or business rules
        
		return queryset
    
	def list(self, request, *args, **kwargs):
		"""
		Override list method to provide enhanced response with query metadata.
        
		Args:
			request (Request): The HTTP request object
            
		Returns:
			Response: Enhanced response with query metadata
		"""
		response = super().list(request, *args, **kwargs)
        
		# Add query metadata to the response
		response.data['query_metadata'] = {
			'total_count': self.get_queryset().count(),
			'filtered_count': self.filter_queryset(self.get_queryset()).count(),
			'filters_available': {
				'exact_match': ['title', 'author', 'publication_year'],
				'partial_match': ['title_contains', 'author_name'],
				'range_filters': ['publication_year_min', 'publication_year_max', 'publication_year_range'],
				'combined_filters': ['title_or_author'],
			},
			'search_fields': self.search_fields,
			'ordering_fields': self.ordering_fields,
			'default_ordering': self.ordering,
		}
        
		return response


class BookAdvancedSearchView(generics.ListAPIView):
	"""
	Advanced search view with universal search capabilities.
    
	This view provides a powerful search experience combining
	multiple search strategies and advanced filtering options.
    
	Features:
	- Universal search across multiple fields
	- Intelligent type detection (text vs numeric)
	- Combined search and filtering
	- Flexible result ordering
    
	Example queries:
	GET /api/books/advanced-search/?q=harry+potter
	GET /api/books/advanced-search/?q=1997&ordering=-created_at
	"""
    
	queryset = Book.objects.select_related('author').all()
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]
	filterset_class = AdvancedBookSearchFilter
    
	filter_backends = [DjangoFilterBackend, OrderingFilter]
	ordering_fields = ['title', 'publication_year', 'created_at']
	ordering = ['-created_at']  # Default to newest first for search results
    
	def list(self, request, *args, **kwargs):
		"""
		Custom list method for advanced search with enhanced response.
		"""
		response = super().list(request, *args, **kwargs)
        
		# Add search metadata
		search_query = request.GET.get('q', '')
		if search_query:
			response.data['search_metadata'] = {
				'query': search_query,
				'results_count': len(response.data['results']) if 'results' in response.data else len(response.data),
				'search_type': 'advanced',
				'fields_searched': ['title', 'author__name', 'publication_year']
			}
        
		return response


class BookFilterOptionsView(generics.GenericAPIView):
	"""
	API endpoint to retrieve available filter options and metadata.
    
	This view helps API consumers discover available filtering,
	searching, and ordering options programmatically.
	"""
    
	permission_classes = [permissions.AllowAny]
    
	def get(self, request, *args, **kwargs):
		"""
		Provide filter configuration and options to API consumers.
        
		Returns:
			Response: Comprehensive filter options metadata
		"""
		filter_options = {
			'filtering': {
				'exact_match': {
					'title': 'Exact book title match',
					'author': 'Author ID (exact match)',
					'publication_year': 'Exact publication year',
				},
				'partial_match': {
					'title_contains': 'Case-insensitive title contains',
					'author_name': 'Case-insensitive author name contains',
				},
				'range_filters': {
					'publication_year_min': 'Books published in or after year',
					'publication_year_max': 'Books published in or before year',
					'publication_year_range': 'Books published within year range (use _min and _max suffixes)',
				},
				'combined_filters': {
					'title_or_author': 'Search in both title and author name fields',
				}
			},
			'searching': {
				'search_parameter': 'search',
				'search_fields': [
					'title (partial match)',
					'author__name (partial match)',
					'publication_year (exact match)',
				],
				'example': '/api/books/?search=harry'
			},
			'ordering': {
				'ordering_parameter': 'ordering',
				'available_fields': [
					'title', '-title',
					'publication_year', '-publication_year', 
					'created_at', '-created_at',
					'author__name', '-author__name',
				],
				'default_ordering': 'title',
				'example': '/api/books/?ordering=-publication_year,title'
			},
			'pagination': {
				'page_parameter': 'page',
				'page_size_parameter': 'page_size',
				'default_page_size': 20,
				'max_page_size': 100,
			}
		}
        
		return Response(filter_options)
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
