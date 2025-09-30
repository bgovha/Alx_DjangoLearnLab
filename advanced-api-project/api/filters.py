"""
Custom filter classes for advanced query capabilities.

This module defines custom filters for the Book model that provide
enhanced filtering, searching, and ordering functionality beyond
the basic DRF capabilities.
"""

import django_filters
from django.db.models import Q
from .models import Book, Author


class BookFilter(django_filters.FilterSet):
    """
    Advanced filter class for Book model with custom filtering capabilities.
    
    This filter set provides:
    - Exact match filtering on specific fields
    - Range filtering for numeric fields
    - Custom lookup expressions
    - Combined filtering logic
    """
    
    # Exact match filters
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='exact',
        help_text="Exact match for book title"
    )
    
    title_contains = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        help_text="Case-insensitive partial match for book title"
    )
    
    author = django_filters.ModelChoiceFilter(
        queryset=Author.objects.all(),
        field_name='author',
        help_text="Filter by specific author ID"
    )
    
    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        help_text="Case-insensitive partial match for author name"
    )
    
    # Range filters for publication year
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='exact',
        help_text="Exact publication year"
    )
    
    publication_year_min = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        help_text="Books published in or after this year"
    )
    
    publication_year_max = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        help_text="Books published in or before this year"
    )
    
    publication_year_range = django_filters.RangeFilter(
        field_name='publication_year',
        help_text="Books published within a year range (e.g., publication_year_range_min=2000&publication_year_range_max=2010)"
    )
    
    # Combined filters
    title_or_author = django_filters.CharFilter(
        method='filter_title_or_author',
        help_text="Search in both title and author name fields"
    )
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'publication_year': ['exact', 'gte', 'lte'],
        }
    
    def filter_title_or_author(self, queryset, name, value):
        """
        Custom filter method to search in both title and author name fields.
        
        Args:
            queryset (QuerySet): The original queryset
            name (str): The filter field name
            value (str): The search value
            
        Returns:
            QuerySet: Filtered queryset containing matches in title or author name
        """
        if value:
            return queryset.filter(
                Q(title__icontains=value) | Q(author__name__icontains=value)
            )
        return queryset
    
    def filter_queryset(self, queryset):
        """
        Override the default filtering to add custom logic.
        
        Args:
            queryset (QuerySet): The original queryset
            
        Returns:
            QuerySet: The filtered queryset with all applied filters
        """
        queryset = super().filter_queryset(queryset)
        
        # Add any additional custom filtering logic here
        return queryset


class AdvancedBookSearchFilter(django_filters.FilterSet):
    """
    Advanced search filter with combined search capabilities.
    
    This filter provides a comprehensive search experience
    combining multiple search strategies and filters.
    """
    
    q = django_filters.CharFilter(
        method='universal_search',
        help_text="Universal search across multiple fields"
    )
    
    def universal_search(self, queryset, name, value):
        """
        Perform universal search across title, author name, and publication year.
        
        Args:
            queryset (QuerySet): The original queryset
            name (str): The filter field name
            value (str): The search value
            
        Returns:
            QuerySet: Filtered queryset with universal search applied
        """
        if value:
            # Try to convert to integer for publication year search
            try:
                year_value = int(value)
                year_query = Q(publication_year=year_value)
            except (ValueError, TypeError):
                year_query = Q()
            
            # Text search query
            text_query = (
                Q(title__icontains=value) |
                Q(author__name__icontains=value)
            )
            
            # Combine both queries
            return queryset.filter(text_query | year_query)
        return queryset
    
    class Meta:
        model = Book
        fields = ['q']
        