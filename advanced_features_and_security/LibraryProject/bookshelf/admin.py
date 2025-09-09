from django.contrib import admin
from .models import Book

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth'),
        }),
    )
    
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(CustomUser, CustomUserAdmin)

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
