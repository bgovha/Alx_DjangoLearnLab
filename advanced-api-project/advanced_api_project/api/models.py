"""
Data models for the API application.

This module defines the Author and Book models which represent
the core data structure of our library management system.
"""

from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    
    Attributes:
        name (CharField): The name of the author (max 100 characters)
        created_at (DateTimeField): Timestamp when the author record was created
        updated_at (DateTimeField): Timestamp when the author record was last updated
    """

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']  # Default ordering by author name
    
    def __str__(self):
        """String representation of the Author model."""
        return self.name

class Book(models.Model):
    """
    Book model representing a published book.
    
    Attributes:
        title (CharField): The title of the book (max 200 characters)
        publication_year (IntegerField): The year the book was published
        author (ForeignKey): Reference to the Author model (one-to-many relationship)
        created_at (DateTimeField): Timestamp when the book record was created
        updated_at (DateTimeField): Timestamp when the book record was last updated
    
    Relationships:
        - Each Book has one Author (ForeignKey)
        - Each Author can have multiple Books (one-to-many)
    """

    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,  # Delete books when author is deleted
        related_name='books'  # Access books via author.books
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['title']  # Default ordering by book title
        unique_together = ['title', 'author']  # Prevent duplicate books by same author
    
    def __str__(self):
        """String representation of the Book model."""
        return f"{self.title} by {self.author.name}"
