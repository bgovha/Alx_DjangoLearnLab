"""
Custom serializers for the API application.

This module defines serializers that handle complex data structures
and nested relationships between Author and Book models.
"""

from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model that includes custom validation.
    
    This serializer handles:
    - Serialization of all Book model fields
    - Custom validation for publication_year
    - Nested author information
    
    Validation:
    - Ensures publication_year is not in the future
    - Validates publication_year is reasonable (after 1000)
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the year is in the future or invalid
        """
        current_year = timezone.now().year
        
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        if value < 1000:
            raise serializers.ValidationError(
                "Publication year should be a reasonable value (after 1000)."
            )
        
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested book relationships.
    
    This serializer handles:
    - Serialization of author details
    - Dynamic nested serialization of related books
    - Control over book serialization depth via context
    
    Nested Relationships:
    - books: A nested list of BookSerializer instances
    - The depth of nested serialization can be controlled via context
    """
    
    # Nested serializer for related books
    books = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'books']
    
    def get_books(self, obj):
        """
        Dynamically serialize related books based on context.
        
        Args:
            obj (Author): The Author instance being serialized
            
        Returns:
            list: Serialized book data or None based on context
        """
        # Check if we should include nested books (controlled via context)
        include_books = self.context.get('include_books', True)
        
        if include_books:
            books = obj.books.all()
            serializer = BookSerializer(books, many=True, context=self.context)
            return serializer.data
        return None
    
    def to_representation(self, instance):
        """
        Custom representation to handle nested relationships dynamically.
        
        Args:
            instance (Author): The Author instance to serialize
            
        Returns:
            dict: The serialized author data
        """
        representation = super().to_representation(instance)
        
        # Remove books field if it's None (when include_books is False)
        if representation['books'] is None:
            representation.pop('books')
            
        return representation

class AuthorDetailSerializer(AuthorSerializer):
    """
    Detailed serializer for Author with full book information.
    
    Extends AuthorSerializer to always include complete book details.
    Useful for detailed author views where book information is essential.
    """
    
    def get_books(self, obj):
        """Always include complete book details in detailed view."""
        books = obj.books.all()
        serializer = BookSerializer(books, many=True, context=self.context)
        return serializer.data