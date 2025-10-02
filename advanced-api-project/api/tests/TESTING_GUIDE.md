"""
Testing Guide for Django REST Framework API

This document provides comprehensive guidance on running and understanding
the test suite for the advanced-api-project.

## Test Structure

The test suite is organized into several test case classes:

1. `BookListViewTests` - Tests for book list and create operations
2. `BookDetailViewTests` - Tests for book retrieve, update, delete operations
3. `BookFilteringSearchingOrderingTests` - Tests for query capabilities
4. `AuthorViewTests` - Tests for author CRUD operations
5. `PaginationTests` - Tests for pagination functionality
6. `ErrorHandlingTests` - Tests for error scenarios and edge cases

## Running Tests

### Run All Tests
```bash
python manage.py test api