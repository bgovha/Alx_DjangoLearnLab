from myapp.models import Book

new_book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

print(f"Created book: {new_book}")
print(f"Book ID: {new_book.id}")

book_count = Book.objects.count()
print(f"Total books in database: {book_count}")