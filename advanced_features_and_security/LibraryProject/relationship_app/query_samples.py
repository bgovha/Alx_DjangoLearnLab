#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create sample data for testing queries"""
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George R.R. Martin")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="A Game of Thrones", author=author2)
    book4 = Book.objects.create(title="A Clash of Kings", author=author2)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="City Library")
    
    # Add books to libraries
    library1.books.add(book1, book2, book3)
    library2.books.add(book3, book4)
    
    # Create librarians
    librarian1 = Librarian.objects.create(name="Alice Johnson", library=library1)
    librarian2 = Librarian.objects.create(name="Bob Smith", library=library2)
    
    return author1, author2, library1, library2

def query_all_books_by_author(author_name):
    """Query all books by a specific author"""
    try:
        #author = Author.objects.get(name=author_name)
        author = Author.objects.filter(author=author).first()
        books = author.books.all()
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found")
        return []

def list_all_books_in_library(library_name):
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name}:")
        for book in books:
            print(f"- {book.title} (by {book.author.name})")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found")
        return []

def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian for a library"""
    try:
        library = Library.objects.get(name=library_name)
        #librarian = Librarian.objects.filter(library=library).first()
        librarian = Librarian.objects.get(library=library).first()
        
        if librarian:
            print(f"Librarian for {library_name}: {librarian.name}")
        else:
            print(f"No librarian assigned to {library_name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found")
        return None
    except AttributeError:
        print(f"No librarian assigned to {library_name}")
        return None

if __name__ == "__main__":
    print("Creating sample data...")
    author1, author2, library1, library2 = create_sample_data()
    
    print("\n" + "="*50)
    print("DEMONSTRATING QUERIES:")
    print("="*50)
    
    # Query 1: All books by a specific author
    print("\n1. Query all books by a specific author:")
    query_all_books_by_author("J.K. Rowling")
    
    # Query 2: List all books in a library
    print("\n2. List all books in a library:")
    list_all_books_in_library("Central Library")
    
    # Query 3: Retrieve librarian for a library
    print("\n3. Retrieve librarian for a library:")
    retrieve_librarian_for_library("Central Library")
    
    print("\n" + "="*50)
    print("QUERY COMPLETED SUCCESSFULLY!")
    print("="*50)