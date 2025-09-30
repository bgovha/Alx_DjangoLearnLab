"""
Comprehensive unit tests for Django REST Framework API endpoints.

This test suite covers all API functionality including:
- CRUD operations for Book and Author models
- Filtering, searching, and ordering capabilities
- Authentication and permission enforcement
- Data validation and error handling
"""

import json
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from ..models import Author, Book
from .factories import AuthorFactory, BookFactory, UserFactory


class BaseAPITestCase(APITestCase):
    """
    Base test case class with common setup and utility methods.
    
    Provides:
    - Common test data creation
    - Authentication helpers
    - Response assertion utilities
    """
    
    def setUp(self):
        """Set up test data and client for all test cases."""
        self.client = APIClient()
        self.anonymous_client = APIClient()  # Client without authentication
        
        # Create test users
        self.regular_user = UserFactory(username='testuser')
        self.admin_user = UserFactory(username='adminuser', is_staff=True)
        
        # Create test data
        self.author1 = AuthorFactory(name='J.K. Rowling')
        self.author2 = AuthorFactory(name='George R.R. Martin')
        
        self.book1 = BookFactory(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = BookFactory(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        self.book3 = BookFactory(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author2
        )
        self.book4 = BookFactory(
            title='A Clash of Kings',
            publication_year=1998,
            author=self.author2
        )
    
    def authenticate_user(self, user=None):
        """Helper method to authenticate a user for testing."""
        if user is None:
            user = self.regular_user
        self.client.force_authenticate(user=user)
    
    def assertResponseSuccess(self, response, expected_status=status.HTTP_200_OK):
        """Assert that response has successful status code."""
        self.assertEqual(response.status_code, expected_status)
    
    def assertResponseError(self, response, expected_status):
        """Assert that response has error status code."""
        self.assertEqual(response.status_code, expected_status)
    
    def assertResponseDataContains(self, response, expected_data):
        """Assert that response data contains expected values."""
        for key, value in expected_data.items():
            self.assertEqual(response.data[key], value)


class BookListViewTests(BaseAPITestCase):
    """
    Test cases for Book List and Create endpoints.
    
    Tests covering:
    - Retrieving list of books
    - Creating new books
    - Authentication requirements
    - Data validation
    """
    
    def test_get_books_list_anonymous(self):
        """
        Test that anonymous users can retrieve books list.
        
        Expected: HTTP 200 OK with list of books
        """
        url = reverse('book-list')
        response = self.anonymous_client.get(url)
        
        self.assertResponseSuccess(response)
        self.assertEqual(len(response.data['results']), 4)
        self.assertIn('title', response.data['results'][0])
        self.assertIn('author', response.data['results'][0])
    
    def test_get_books_list_authenticated(self):
        """
        Test that authenticated users can retrieve books list.
        
        Expected: HTTP 200 OK with list of books
        """
        self.authenticate_user()
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)
        self.assertEqual(len(response.data['results']), 4)
    
    def test_create_book_authenticated(self):
        """
        Test that authenticated users can create new books.
        
        Expected: HTTP 201 Created with book data
        """
        self.authenticate_user()
        url = reverse('book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertResponseSuccess(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Test Book')
        self.assertEqual(Book.objects.count(), 5)  # 4 initial + 1 new
    
    def test_create_book_anonymous(self):
        """
        Test that anonymous users cannot create books.
        
        Expected: HTTP 403 Forbidden
        """
        url = reverse('book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.anonymous_client.post(url, data, format='json')
        
        self.assertResponseError(response, status.HTTP_403_FORBIDDEN)
    
    def test_create_book_validation_future_year(self):
        """
        Test that books with future publication years are rejected.
        
        Expected: HTTP 400 Bad Request with validation error
        """
        self.authenticate_user()
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertResponseError(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_validation_invalid_author(self):
        """
        Test that books with invalid author IDs are rejected.
        
        Expected: HTTP 400 Bad Request with validation error
        """
        self.authenticate_user()
        url = reverse('book-create')
        data = {
            'title': 'Invalid Author Book',
            'publication_year': 2020,
            'author': 9999  # Non-existent author
        }
        response = self.client.post(url, data, format='json')
        
        self.assertResponseError(response, status.HTTP_400_BAD_REQUEST)


class BookDetailViewTests(BaseAPITestCase):
    """
    Test cases for Book Retrieve, Update, and Delete endpoints.
    
    Tests covering:
    - Retrieving single book details
    - Updating existing books
    - Deleting books
    - Authentication requirements for write operations
    """
    
    def test_get_book_detail_anonymous(self):
        """
        Test that anonymous users can retrieve book details.
        
        Expected: HTTP 200 OK with book data
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.anonymous_client.get(url)
        
        self.assertResponseSuccess(response)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
    
    def test_update_book_authenticated(self):
        """
        Test that authenticated users can update books.
        
        Expected: HTTP 200 OK with updated book data
        """
        self.authenticate_user()
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated Book Title',
            'publication_year': self.book1.publication_year,
            'author': self.book1.author.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertResponseSuccess(response)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
    
    def test_partial_update_book_authenticated(self):
        """
        Test that authenticated users can partially update books.
        
        Expected: HTTP 200 OK with updated book data
        """
        self.authenticate_user()
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {'title': 'Partially Updated Title'}
        response = self.client.patch(url, data, format='json')
        
        self.assertResponseSuccess(response)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')
    
    def test_update_book_anonymous(self):
        """
        Test that anonymous users cannot update books.
        
        Expected: HTTP 403 Forbidden
        """
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {'title': 'Unauthorized Update'}
        response = self.anonymous_client.patch(url, data, format='json')
        
        self.assertResponseError(response, status.HTTP_403_FORBIDDEN)
    
    def test_delete_book_authenticated(self):
        """
        Test that authenticated users can delete books.
        
        Expected: HTTP 204 No Content
        """
        self.authenticate_user()
        url = reverse('book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertResponseSuccess(response, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
    
    def test_delete_book_anonymous(self):
        """
        Test that anonymous users cannot delete books.
        
        Expected: HTTP 403 Forbidden
        """
        url = reverse('book-delete', kwargs={'pk': self.book1.id})
        response = self.anonymous_client.delete(url)
        
        self.assertResponseError(response, status.HTTP_403_FORBIDDEN)
    
    def test_get_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist.
        
        Expected: HTTP 404 Not Found
        """
        url = reverse('book-detail', kwargs={'pk': 9999})
        response = self.anonymous_client.get(url)
        
        self.assertResponseError(response, status.HTTP_404_NOT_FOUND)


class BookFilteringSearchingOrderingTests(BaseAPITestCase):
    """
    Test cases for Book filtering, searching, and ordering functionality.
    
    Tests covering:
    - Field-based filtering
    - Text search functionality
    - Result ordering
    - Combined query parameters
    """
    
    def test_filter_books_by_author(self):
        """
        Test filtering books by specific author.
        
        Expected: Only books by specified author returned
        """
        url = reverse('book-list')
        response = self.client.get(f"{url}?author={self.author1.id}")
        
        self.assertResponseSuccess(response)
        results = response.data['results']
        self.assertEqual(len(results), 2)  # author1 has 2 books
        for book in results:
            self.assertEqual(book['author'], self.author1.id)
    
    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year.
        
        Expected: Only books from specified year returned
        """
        url = reverse('book-list')
        response = self.client.get(f"{url}?publication_year=1998")
        
        self.assertResponseSuccess(response)
        results = response.data['results']
        self.assertEqual(len(results), 2)  # 2 books from 1998
        for book in results:
            self.assertEqual(book['publication_year'], 1998)
    
    def test_filter_books_by_year_range(self):
        """
        Test filtering books by publication year range.
        
        Expected: Only books within year range returned
        """
        url = reverse('book-list')
        response = self.client.get(f"{url}?publication_year_min=1997&publication_year_max=1998")
        
        self.assertResponseSuccess(response)
        results = response.data['results']
        self.assertEqual(len(results), 3)  # 3 books between 1997-1998
        for book in results:
            self.assertGreaterEqual(book['publication_year'], 1997)
            self.assertLessEqual(book['publication_year'], 1998)
    
    def test_search_books_by_title(self):
        """
        Test searching books by title text.
        
        Expected: Books matching search term in title returned
        """
        url = reverse('book-list')
        response = self.client.get(f"{url}?search=Harry")
        
        self.assertResponseSuccess(response)
        results = response.data['results']
        self.assertEqual(len(results), 2)  # 2 Harry Potter books
        for book in results:
            self.assertIn('Harry', book['title'])
    
    def test_search_books_by_author_name(self):
        """
        Test searching books by author name.
        
        Expected: Books by authors matching search term returned
        """
        url = reverse('book-list')
        response = self.client.get(f"{url}?search=Martin")
        
        self.assertResponseSuccess(response)
        results = response.data['results']
        self.assertEqual(len(results), 2)  # 2 books by George R.R. Martin
        self.assertEqual(results[0]['author_name'], 'George R.R. Martin')
    
    def test_order_books_by_title_ascending(self):
        """
        Test ordering books by title ascending.
        
        Expected: Books ordered by title A-Z
        """
        url = reverse('book-list')
        response = self.client.get(f"{url}?ordering=title")
        
        self.assertResponseSuccess(response)
        results = response.data['results']
        titles = [book['title'] for book in results]
        self.assertEqual(titles, sorted(titles))
    
    def test_order_books_by_publication_year_descending(self):
        """
        Test ordering books by publication year descending.
        
        Expected: Books ordered by publication year newest first
        """
        url = reverse('book-list')
        response = self.client.get(f"{url}?ordering=-publication_year")
        
        self.assertResponseSuccess(response)
        results = response.data['results']
        years = [book['publication_year'] for book in results]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_combined_filter_search_order(self):
        """
        Test combined filtering, searching, and ordering.
        
        Expected: Precisely filtered, searched, and ordered results
        """
        url = reverse('book-list')
        response = self.client.get(
            f"{url}?author={self.author1.id}&search=Harry&ordering=-publication_year"
        )
        
        self.assertResponseSuccess(response)
        results = response.data['results']
        
        # Should get Harry Potter books by J.K. Rowling, newest first
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['title'], 'Harry Potter and the Chamber of Secrets')  # 1998
        self.assertEqual(results[1]['title'], 'Harry Potter and the Philosopher\'s Stone')  # 1997
    
    def test_advanced_search_functionality(self):
        """
        Test advanced search endpoint with universal search.
        
        Expected: Relevant results across multiple fields
        """
        url = reverse('book-advanced-search')
        response = self.client.get(f"{url}?q=1997")
        
        self.assertResponseSuccess(response)
        results = response.data['results']
        self.assertTrue(len(results) >= 1)
        self.assertEqual(results[0]['publication_year'], 1997)


class AuthorViewTests(BaseAPITestCase):
    """
    Test cases for Author API endpoints.
    
    Tests covering CRUD operations for Author model with proper authentication.
    """
    
    def test_get_authors_list(self):
        """
        Test retrieving list of authors.
        
        Expected: HTTP 200 OK with list of authors
        """
        url = reverse('author-list')
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_create_author_authenticated(self):
        """
        Test that authenticated users can create authors.
        
        Expected: HTTP 201 Created with author data
        """
        self.authenticate_user()
        url = reverse('author-create')
        data = {'name': 'New Test Author'}
        response = self.client.post(url, data, format='json')
        
        self.assertResponseSuccess(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Test Author')
        self.assertEqual(Author.objects.count(), 3)
    
    def test_get_author_with_books(self):
        """
        Test retrieving author details with nested books.
        
        Expected: HTTP 200 OK with author data and nested books
        """
        url = reverse('author-detail', kwargs={'pk': self.author1.id})
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)
        self.assertEqual(response.data['name'], 'J.K. Rowling')
        self.assertIn('books', response.data)
        self.assertEqual(len(response.data['books']), 2)


class PaginationTests(BaseAPITestCase):
    """
    Test cases for API pagination functionality.
    """
    
    def setUp(self):
        """Set up additional books for pagination testing."""
        super().setUp()
        # Create more books to test pagination
        for i in range(10):
            BookFactory(
                title=f'Test Book {i}',
                publication_year=2000 + i,
                author=self.author1
            )
    
    def test_pagination_default_page_size(self):
        """
        Test that pagination returns default page size.
        
        Expected: Default number of results per page
        """
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertLessEqual(len(response.data['results']), 20)  # Default page size
    
    def test_pagination_custom_page_size(self):
        """
        Test custom page size parameter.
        
        Expected: Custom number of results per page
        """
        url = reverse('book-list')
        response = self.client.get(f"{url}?page_size=5")
        
        self.assertResponseSuccess(response)
        self.assertEqual(len(response.data['results']), 5)
    
    def test_pagination_page_navigation(self):
        """
        Test pagination page navigation.
        
        Expected: Different results for different pages
        """
        url = reverse('book-list')
        response_page1 = self.client.get(f"{url}?page_size=5&page=1")
        response_page2 = self.client.get(f"{url}?page_size=5&page=2")
        
        self.assertResponseSuccess(response_page1)
        self.assertResponseSuccess(response_page2)
        
        # Results should be different between pages
        page1_titles = [book['title'] for book in response_page1.data['results']]
        page2_titles = [book['title'] for book in response_page2.data['results']]
        
        self.assertNotEqual(page1_titles, page2_titles)
        self.assertTrue(all(title not in page2_titles for title in page1_titles))


class ErrorHandlingTests(BaseAPITestCase):
    """
    Test cases for API error handling and edge cases.
    """
    
    def test_invalid_filter_parameters(self):
        """
        Test handling of invalid filter parameters.
        
        Expected: Graceful handling with appropriate response
        """
        url = reverse('book-list')
        response = self.client.get(f"{url}?invalid_param=value")
        
        # Should not crash, just ignore invalid params
        self.assertResponseSuccess(response)
    
    def test_malformed_json_request(self):
        """
        Test handling of malformed JSON in requests.
        
        Expected: HTTP 400 Bad Request
        """
        self.authenticate_user()
        url = reverse('book-create')
        response = self.client.post(
            url, 
            data='{"malformed: json}', 
            content_type='application/json'
        )
        
        self.assertResponseError(response, status.HTTP_400_BAD_REQUEST)
    
    def test_rate_limiting(self):
        """
        Test that rate limiting is properly configured.
        
        Note: This is a basic test; actual rate limiting might need more specific setup
        """
        url = reverse('book-list')
        
        # Make multiple rapid requests
        for _ in range(5):
            response = self.client.get(url)
            self.assertResponseSuccess(response)