from django.urls import path
from . import views
from .views import BookList

urlpatterns = [
    path('', views.api_overview, name='api-overview'),
    path('books/', BookList.as_view(), name='book-list'),  # Maps to the BookList view
]