from myapp.models import Book

# Retrieve the book first
book = Book.objects.get(id=1)
print(f"Original title: {book.title}")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()  # Don't forget to save!

print(f"Updated title: {book.title}")

# Verify the update
updated_book = Book.objects.get(id=1)
print(f"Verified updated title: {updated_book.title}")

# Alternative: Update using QuerySet (single operation)
Book.objects.filter(id=1).update(title="Nineteen Eighty-Four")

# Verify the second update
final_book = Book.objects.get(id=1)
print(f"Final title: {final_book.title}")