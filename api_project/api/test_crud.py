import requests

BASE_URL = 'http://127.0.0.1:8000/api/books_all/'

def test_crud_operations():
    # 1. Create a new book
    print("1. Creating a new book...")
    new_book = {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger"
    }
    response = requests.post(BASE_URL, json=new_book)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Get the ID of the created book
    book_id = response.json()['id']
    
    # 2. Retrieve the created book
    print(f"\n2. Retrieving book with ID {book_id}...")
    response = requests.get(f"{BASE_URL}{book_id}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 3. Update the book
    print(f"\n3. Updating book with ID {book_id}...")
    updated_book = {
        "title": "The Catcher in the Rye - Special Edition",
        "author": "J.D. Salinger"
    }
    response = requests.put(f"{BASE_URL}{book_id}/", json=updated_book)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 4. Partial update
    print(f"\n4. Partially updating book with ID {book_id}...")
    partial_update = {
        "title": "The Catcher in the Rye - Revised"
    }
    response = requests.patch(f"{BASE_URL}{book_id}/", json=partial_update)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 5. List all books
    print("\n5. Listing all books...")
    response = requests.get(BASE_URL)
    print(f"Status: {response.status_code}")
    print(f"Number of books: {len(response.json())}")
    
    # 6. Delete the book
    print(f"\n6. Deleting book with ID {book_id}...")
    response = requests.delete(f"{BASE_URL}{book_id}/")
    print(f"Status: {response.status_code}")
    
    # 7. Verify deletion
    print(f"\n7. Verifying book with ID {book_id} is deleted...")
    response = requests.get(f"{BASE_URL}{book_id}/")
    print(f"Status: {response.status_code}")

if __name__ == "__main__":
    test_crud_operations()