"""
Comprehensive testing script for filtering, searching, and ordering capabilities.

Use this script to manually test all advanced query features of the Book API.
Test using curl, Postman, or any API testing tool.
"""

# Base URL for testing
BASE_URL = "http://localhost:8000/api"

# Example test queries for filtering, searching, and ordering

FILTERING_EXAMPLES = """
# FILTERING EXAMPLES:

# 1. Exact title match
curl "{base}/books/?title=Harry%20Potter"

# 2. Partial title match (case-insensitive)
curl "{base}/books/?title_contains=harry"

# 3. Filter by author ID
curl "{base}/books/?author=1"

# 4. Filter by author name (partial match)
curl "{base}/books/?author_name=rowling"

# 5. Exact publication year
curl "{base}/books/?publication_year=1997"

# 6. Books published after certain year
curl "{base}/books/?publication_year_min=2000"

# 7. Books published before certain year
curl "{base}/books/?publication_year_max=2010"

# 8. Books published within year range
curl "{base}/books/?publication_year_range_min=1990&publication_year_range_max=2000"

# 9. Combined search in title or author name
curl "{base}/books/?title_or_author=potter"

# 10. Multiple filters combined
curl "{base}/books/?title_contains=harry&publication_year_min=1990&publication_year_max=2000"
""".format(base=BASE_URL)

SEARCHING_EXAMPLES = """
# SEARCHING EXAMPLES:

# 1. Basic search across title and author name
curl "{base}/books/?search=rowling"

# 2. Search with multiple terms
curl "{base}/books/?search=harry%20potter"

# 3. Search with publication year
curl "{base}/books/?search=1997"

# 4. Advanced universal search
curl "{base}/books/advanced-search/?q=harry%20potter"

# 5. Advanced search with numeric value
curl "{base}/books/advanced-search/?q=1997"
""".format(base=BASE_URL)

ORDERING_EXAMPLES = """
# ORDERING EXAMPLES:

# 1. Order by title (ascending - default)
curl "{base}/books/?ordering=title"

# 2. Order by title (descending)
curl "{base}/books/?ordering=-title"

# 3. Order by publication year (newest first)
curl "{base}/books/?ordering=-publication_year"

# 4. Order by publication year (oldest first)
curl "{base}/books/?ordering=publication_year"

# 5. Order by multiple fields (publication year descending, then title ascending)
curl "{base}/books/?ordering=-publication_year,title"

# 6. Order by author name
curl "{base}/books/?ordering=author__name"

# 7. Combined filtering and ordering
curl "{base}/books/?title_contains=harry&ordering=-publication_year"
""".format(base=BASE_URL)

COMBINED_EXAMPLES = """
# COMBINED QUERY EXAMPLES:

# 1. Filter, search, and order combined
curl "{base}/books/?title_contains=harry&search=rowling&ordering=-publication_year"

# 2. Multiple filters with ordering
curl "{base}/books/?publication_year_min=1990&publication_year_max=2000&author_name=rowling&ordering=title"

# 3. Get filter options
curl "{base}/books/filter-options/"

# 4. Pagination with filtering
curl "{base}/books/?title_contains=book&page=2&page_size=10"
""".format(base=BASE_URL)

if __name__ == "__main__":
    print("FILTERING, SEARCHING, AND ORDERING TEST EXAMPLES")
    print("=" * 50)
    print(FILTERING_EXAMPLES)
    print(SEARCHING_EXAMPLES)
    print(ORDERING_EXAMPLES)
    print(COMBINED_EXAMPLES)
    