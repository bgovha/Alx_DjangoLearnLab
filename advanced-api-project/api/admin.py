
"""
Admin configuration for the API models.
"""

from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	"""Admin configuration for Author model."""
	list_display = ['name', 'created_at', 'updated_at']
	search_fields = ['name']
	list_filter = ['created_at']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	"""Admin configuration for Book model."""
	list_display = ['title', 'author', 'publication_year', 'created_at']
	list_filter = ['publication_year', 'author', 'created_at']
	search_fields = ['title', 'author__name']
	autocomplete_fields = ['author']
