from bookshelf.models import Book

# Check current count
initial_count = Book.objects.count()
print(f"Books before deletion: {initial_count}")

# Retrieve and delete the book
book = Book.objects.get(id=1)
print(f"Book to delete: {book}")

book.delete()  # This deletes the record

# Verify deletion
final_count = Book.objects.count()
print(f"Books after deletion: {final_count}")

# Try to retrieve the deleted book
try:
    deleted_book = Book.objects.get(id=1)
    print(f"Unexpectedly found: {deleted_book}")
except Book.DoesNotExist:
    print("Book successfully deleted - cannot be found anymore")