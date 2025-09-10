from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.exceptions import ValidationError
from django.utils.html import escape
from .models import Book
from .forms import ExampleForm

def safe_search(query):
    """
    Safe search function that prevents SQL injection by using Django's ORM
    and properly escapes user input to prevent XSS.
    """
    if not query or not query.strip():
        return Book.objects.none()
    
    # Escape user input to prevent XSS in search results display
    safe_query = escape(query.strip())
    
    # Use Django's ORM with parameterized queries
    return Book.objects.filter(
        Q(title__icontains=safe_query) |
        Q(author__icontains=safe_query) |
        Q(isbn__iexact=safe_query)
    )

@login_required
def book_list(request):
    """
    Secure book listing with safe search functionality.
    """
    books = Book.objects.all()
    search_query = request.GET.get('q', '')
    
    if search_query:
        books = safe_search(search_query)
    
    context = {
        'books': books,
        'search_query': search_query,
    }
    return render(request, 'bookshelf/book_list.html', context)

@login_required
@permission_required('bookshelf.add_book', raise_exception=True)
def book_create(request):
    """
    Secure book creation with form validation and CSRF protection.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Additional server-side validation
            book = form.save(commit=False)
            try:
                book.full_clean()  # Run model validation
                book.save()
                return redirect('book_list')
            except ValidationError as e:
                # Add validation errors to form
                for field, errors in e.error_dict.items():
                    for error in errors:
                        form.add_error(field, error)
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})

@login_required
@permission_required('bookshelf.change_book', raise_exception=True)
def book_update(request, pk):
    """
    Secure book update with proper authorization checks.
    """
    book = get_object_or_404(Book, pk=pk)
    
    # Additional authorization check (example: only owners can edit)
    if not request.user.is_staff and book.owner != request.user:
        return HttpResponseBadRequest("You don't have permission to edit this book.")
    
    if request.method == 'POST':
        form = ExampleForm(request.POST, instance=book)
        if form.is_valid():
            try:
                form.instance.full_clean()
                form.save()
                return redirect('book_list')
            except ValidationError as e:
                for field, errors in e.error_dict.items():
                    for error in errors:
                        form.add_error(field, error)
    else:
        form = ExampleForm(instance=book)
    
    return render(request, 'bookshelf/form_example.html', {'form': form})

@login_required
@permission_required('bookshelf.delete_book', raise_exception=True)
def book_delete(request, pk):
    """
    Secure book deletion with CSRF protection and authorization.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if not request.user.is_staff and book.owner != request.user:
        return HttpResponseBadRequest("You don't have permission to delete this book.")
    
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    
    return render(request, 'bookshelf/confirm_delete.html', {'book': book})

def api_book_search(request):
    """
    Secure API endpoint for book search with input validation.
    """
    if not request.GET.get('q'):
        return JsonResponse({'error': 'Query parameter "q" is required'}, status=400)
    
    query = request.GET.get('q', '')[:100]  # Limit query length
    
    if len(query) < 2:
        return JsonResponse({'error': 'Query must be at least 2 characters long'}, status=400)
    
    books = safe_search(query)
    
    # Return safe data (no HTML, just strings)
    results = [
        {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn
        }
        for book in books[:10]  # Limit results
    ]
    
    return JsonResponse({'results': results})
