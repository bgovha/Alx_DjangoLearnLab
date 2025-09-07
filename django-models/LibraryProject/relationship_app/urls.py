from django.urls import path
from . import views
from .views import list_books
from django.contrib import admin
from django.urls import path, include

app_name = 'relationship_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('relationship/', include('relationship_app.urls')),
    # Function-based view URL
    path('books/', views.list_books, name='list_books'),
    
    # Class-based view URL
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]