from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import DetailView, CreateView
from .models import Library, Book, UserProfile
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth.models import User
from .decorators import admin_required, librarian_required, member_required
from django.utils.decorators import method_decorator

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(LoginRequiredMixin, DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    login_url = 'relationship_app:login'

    def get_object(self):
        return get_object_or_404(Library, pk=self.kwargs['pk'])
@login_required(login_url='relationship_app:login')
def list_books(request):
    books = Book.objects.all().select_related('author')
    libraries = Library.objects.all()
    return render(request, 'relationship_app/list_books.html', {
        'books': books,
        'libraries': libraries
    })

# Authentication Views
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
        messages.success(self.request, 'Registration successful! Please log in.')
        return response   

# Role-based views
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