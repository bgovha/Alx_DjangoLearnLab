# Advanced Django REST Framework API

This project demonstrates advanced API development with Django REST Framework, featuring custom views, permissions, and complex data handling.

## View Configurations

### Book Views

#### BookListView (`GET /api/books/`)
- **Purpose**: Retrieve all books with filtering and search
- **Permissions**: Public read access
- **Features**:
  - Search across title and author name
  - Filter by publication year and author
  - Order by title, publication year, or creation date
  - Pagination support

#### BookCreateView (`POST /api/books/create/`)
- **Purpose**: Create new book instances
- **Permissions**: Authenticated users only
- **Custom Behavior**:
  - Automatic validation using BookSerializer
  - Custom `perform_create` hook for additional processing
  - Publication year validation (cannot be future)

#### BookDetailView (`GET /api/books/<pk>/`)
- **Purpose**: Retrieve specific book details
- **Permissions**: Public read access

#### BookUpdateView (`PUT/PATCH /api/books/<pk>/update/`)
- **Purpose**: Modify existing books
- **Permissions**: Authenticated users only
- **Custom Behavior**:
  - Supports partial updates (PATCH)
  - Custom `perform_update` hook

#### BookDeleteView (`DELETE /api/books/<pk>/delete/`)
- **Purpose**: Remove books from database
- **Permissions**: Authenticated users only
- **Custom Behavior**:
  - Custom response message on deletion
  - Custom `perform_destroy` hook

### Author Views

Similar structure to Book views with appropriate permissions and customization.

### Custom Views

#### BookBulkCreateView (`POST /api/books/bulk-create/`)
- **Purpose**: Create multiple books in single request
- **Permissions**: Authenticated users only
- **Features**:
  - Partial success handling (HTTP 207)
  - Individual validation for each book
  - Detailed error reporting

#### BookSearchView (`GET /api/books/search/`)
- **Purpose**: Advanced book search with multiple criteria
- **Permissions**: Public read access
- **Search Parameters**:
  - `title`: Case-insensitive title search
  - `author_name`: Author name search
  - `year_from`, `year_to`: Publication year range

## Permission Structure

- **Read Operations**: Public access (`AllowAny`)
- **Write Operations**: Authenticated users only (`IsAuthenticated`)
- **Default**: `IsAuthenticatedOrReadOnly` (DRF setting)

## Custom Settings and Hooks

### View Customization Hooks

1. `perform_create()`: Custom logic before saving new instances
2. `perform_update()`: Custom logic before updating instances  
3. `perform_destroy()`: Custom logic before deleting instances
4. `get_queryset()`: Custom query optimization and filtering
5. `get_serializer_context()`: Additional context for serializers

### Filter Backends

- **DjangoFilterBackend**: Field-based filtering
- **SearchFilter**: Full-text search across specified fields
- **OrderingFilter**: Dynamic result ordering

## Testing Guidelines

1. **Public Endpoints**: Test without authentication
2. **Protected Endpoints**: Test with valid credentials
3. **Validation**: Test edge cases and invalid data
4. **Permissions**: Verify access restrictions work correctly
5. **Bulk Operations**: Test partial success scenarios

## API Endpoints Summary

| Endpoint | Method | Purpose | Access |
|----------|--------|---------|---------|
| `/api/books/` | GET | List all books | Public |
| `/api/books/create/` | POST | Create new book | Authenticated |
| `/api/books/<pk>/` | GET | Get book details | Public |
| `/api/books/<pk>/update/` | PUT/PATCH | Update book | Authenticated |
| `/api/books/<pk>/delete/` | DELETE | Delete book | Authenticated |
| `/api/books/bulk-create/` | POST | Bulk create books | Authenticated |
| `/api/books/search/` | GET | Advanced search | Public |

Similar endpoints available for Author model.