from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django import forms
from django.views.generic.detail import DetailView
from .models import Library, Book, UserProfile
from .forms import BookForm
from .decorators import admin_required, librarian_required, member_required

# --- Utility Functions ---

def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'admin'


# --- Authentication Views ---

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('relationship_app:list_books')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return render(request, 'relationship_app/logout.html')


class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role')


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('relationship_app:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        role = form.cleaned_data.get('role')
        user.profile.role = role
        user.profile.save()

        group_name = {
            'admin': 'Admins',
            'librarian': 'Librarians',
            'member': 'Members'
        }.get(role, 'Members')
        group = Group.objects.get(name=group_name)
        user.groups.add(group)

        messages.success(self.request, 'Registration successful! Please log in.')
        return response


# --- Book Views ---

@login_required(login_url='relationship_app:login')
def list_books(request):
    books = Book.objects.all().select_related('author')
    libraries = Library.objects.all()
    return render(request, 'relationship_app/list_books.html', {
        'books': books,
        'libraries': libraries
    })


@login_required
@permission_required('relationship_app.can_view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/book_list.html', {'books': books})


@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('relationship_app:book_list')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {
        'form': form,
        'title': 'Add New Book'
    })


@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('relationship_app:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {
        'form': form,
        'title': f'Edit Book: {book.title}',
        'book': book
    })


@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('relationship_app:book_list')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})


# --- Library Views ---

class LibraryDetailView(LoginRequiredMixin, DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    login_url = 'relationship_app:login'

    def get_object(self):
        return get_object_or_404(Library, pk=self.kwargs['pk'])


# --- Role-based Views ---

@login_required
@admin_required
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@login_required
@librarian_required
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@login_required
@member_required
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


@user_passes_test(is_admin, login_url='relationship_app:login')
def admin_only_view(request):
    return render(request, 'relationship_app/admin_only.html')