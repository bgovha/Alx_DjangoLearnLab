"""
Test factories for creating model instances in tests.

This module provides factory classes to easily create test data
for Author and Book models, ensuring consistent test data generation.
"""

from django.contrib.auth.models import User
from factory import DjangoModelFactory, Faker, SubFactory, post_generation
from factory.fuzzy import FuzzyInteger
import factory
from ..models import Author, Book

class UserFactory(DjangoModelFactory):
    """
    Factory for creating User instances for authentication testing.
    """
    class Meta:
        model = User
    
    username = Faker('user_name')
    email = Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'testpassword123')
    
    @post_generation
    def make_active(self, create, extracted, **kwargs):
        """Make user active by default."""
        self.is_active = True

class AuthorFactory(DjangoModelFactory):
    """
    Factory for creating Author instances with realistic test data.
    """
    class Meta:
        model = Author
    
    name = Faker('name')

class BookFactory(DjangoModelFactory):
    """
    Factory for creating Book instances with realistic test data and proper relationships.
    """
    class Meta:
        model = Book
    
    title = Faker('sentence', nb_words=4)
    publication_year = FuzzyInteger(1900, 2023)  # Random year between 1900-2023
    author = SubFactory(AuthorFactory)
    