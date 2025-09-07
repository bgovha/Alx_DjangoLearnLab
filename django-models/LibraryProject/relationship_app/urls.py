from django.urls import path
from . import views
from .views import list_books
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include


app_name = 'relationship_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('relationship/', include('relationship_app.urls')),
    # Function-based view URL
    path('books/', views.list_books, name='list_books'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    # Class-based view URL
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('login/', views.register.login_view, name='login'),
    path('logout/', views.register.logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),

]