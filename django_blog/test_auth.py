"""
Test Script for Authentication System
Run with: python manage.py shell < test_auth.py
"""

from django.test import Client
from django.contrib.auth.models import User

def test_registration():
    print("Testing Registration...")
    client = Client()
    response = client.post('/users/register/', {
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'complexpassword123',
        'password2': 'complexpassword123',
    })
    print(f"Registration Status: {response.status_code}")
    return response

def test_login():
    print("Testing Login...")
    client = Client()
    response = client.post('/users/login/', {
        'username': 'testuser',
        'password': 'complexpassword123',
    })
    print(f"Login Status: {response.status_code}")
    return response

# Run tests
if __name__ == "__main__":
    test_registration()
    test_login()