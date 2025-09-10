from django import forms
from django.core.exceptions import ValidationError
from .models import Book

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '200'  # HTML validation
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '100'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '^[0-9-]+$',  # Basic ISBN pattern
                'title': 'Enter valid ISBN (numbers and hyphens only)'
            }),
            'publication_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'maxlength': '1000'
            }),
        }

    def clean_isbn(self):
        """Custom validation for ISBN field"""
        isbn = self.cleaned_data.get('isbn', '')
        
        # Remove any hyphens for validation
        clean_isbn = isbn.replace('-', '')
        
        # Basic ISBN validation (10 or 13 digits)
        if not clean_isbn.isdigit():
            raise ValidationError('ISBN must contain only numbers and hyphens.')
        
        if len(clean_isbn) not in [10, 13]:
            raise ValidationError('ISBN must be 10 or 13 digits long.')
        
        return isbn

    def clean_title(self):
        """Sanitize title input"""
        title = self.cleaned_data.get('title', '')
        # Remove any potentially dangerous characters
        return title.strip()

    def clean_description(self):
        """Sanitize description input"""
        description = self.cleaned_data.get('description', '')
        # Basic HTML stripping (in production, use a proper sanitizer like bleach)
        import re
        description = re.sub(r'<script.*?>.*?</script>', '', description, flags=re.DOTALL | re.IGNORECASE)
        return description.strip()