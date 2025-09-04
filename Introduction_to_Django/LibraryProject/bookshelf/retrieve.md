from myapp.models import Book

retrieved_book = Book.objects.get(id=1)
print(f"Retrieved by ID: {retrieved_book}")

retrieved_book = Book.objects.get(title="The Great Gatsby")
print(f"Retrieved by title: {retrieved_book}")

all_books = Book.objects.all()
print(f"All books: {list(all_books)}")

fitzgerald_books = Book.objects.filter(author="F. Scott Fitzgerald")
print(f"Fitzgerald books: {list(fitzgerald_books)}")

try:
    book = Book.objects.get(id=999)  # Non-existent ID
except Book.DoesNotExist:
    print("Book with ID 999 does not exist")

