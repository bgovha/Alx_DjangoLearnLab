from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books

app_name = 'relationship_app'

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # Book views
    path('books/', views.list_books, name='list_books'),
    path('books/manage/', views.book_list, name='book_list'),
    path('books/add_book/', views.add_book, name='add_book'),
    path('books/edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:pk>/', views.delete_book, name='delete_book'),

    # Library views
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Role-based views
    path('admin_view/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
]