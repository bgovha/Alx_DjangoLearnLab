from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Basic configuration
    list_display = ['title', 'author', 'publication_year', 'created_at']
    list_filter = ['author', 'publication_year', 'created_at']
    search_fields = ['title', 'author']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    # Optional: Add fieldsets for better organization in detail view
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'publication_year')
        }),
        ('Additional Information', {
            'fields': ('description', 'isbn', 'genre'),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
    )

# Register your models here.
