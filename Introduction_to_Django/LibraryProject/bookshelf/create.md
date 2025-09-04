from myapp.models import Book

new_book = Book.objects.create(
    title="The Great Gatsby",
    author="F. Scott Fitzgerald",
    publication_year=1925
)

print(f"Created book: {new_book}")
print(f"Book ID: {new_book.id}")