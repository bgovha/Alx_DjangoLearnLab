
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet, PublicBookList
from . import views


# Create a router and register our ViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Public endpoint (no authentication required)
    path('books/public/', PublicBookList.as_view(), name='book-list-public'),
    # Protected endpoint (authentication required)
    path('books/', BookList.as_view(), name='book-list'),
    # Include the router URLs for BookViewSet (with permissions)
    path('', include(router.urls)),
]