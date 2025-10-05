# Django Blog Authentication System

## Overview

This authentication system enables user registration, login, logout, and profile management for a personalized experience in your Django blog project.

## Features

- **User Registration:** Users can sign up with username, email, first/last name, and password. Duplicate emails are prevented.
- **Login/Logout:** Secure login and logout using Django’s built-in views and custom feedback.
- **Profile Management:** Authenticated users can view and update their profile, including bio, location, birth date, and profile picture.
- **Password Reset:** Users can reset their password via email.
- **Security:** All forms use CSRF tokens. Passwords are securely hashed.

## Code Structure

- **models.py:**
  - `Profile` model extends user info with bio, location, birth date, and profile picture.
  - Signals automatically create a profile for each new user.
- **forms.py:**
  - `UserRegisterForm` extends `UserCreationForm` with email and name fields, plus email validation.
  - `UserUpdateForm` and `ProfileUpdateForm` allow profile editing.
- **views.py:**
  - `register`, `profile`, and `CustomLoginView` handle registration, profile management, and login feedback.
- **urls.py:**
  - All authentication URLs are defined in `users/urls.py` and included in the main `urls.py`.
- **templates/users/:**
  - `login.html`, `logout.html`, `register.html`, `profile.html` provide user interfaces, styled with crispy forms and Bootstrap 5.

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install django crispy-bootstrap5 pillow
   ```
2. **Add to `INSTALLED_APPS` in `settings.py`:**
   ```python
   'crispy_forms',
   'crispy_bootstrap5',
   'users',
   ```
3. **Configure crispy forms in `settings.py`:**
   ```python
   CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
   CRISPY_TEMPLATE_PACK = "bootstrap5"
   ```
4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
6. **Collect static files (if needed):**
   ```bash
   python manage.py collectstatic
   ```

## User Guide

- **Register:** Go to `/users/register/` to create an account.
- **Login:** Go to `/users/login/` to sign in.
- **Logout:** Go to `/users/logout/` to log out.
- **Profile:** Go to `/users/profile/` to view and edit your profile.
- **Password Reset:** Use the link on the login page to reset your password.

## Testing

- Automated tests are provided in `test_auth.py` for registration and login.
- To run tests:
  ```bash
  python manage.py test
  ```
- Manual testing:
  - Register a new user and verify email uniqueness.
  - Log in and log out.
  - Edit profile details and upload a profile picture.
  - Reset password using the provided link.

## Security Notes

- All forms use CSRF tokens for protection.
- Passwords are hashed using Django’s built-in algorithms.
- Profile pictures are resized to max 300x300 pixels for safety and performance.

## Extending

- Add more fields to the `Profile` model as needed.
- Customize templates for your branding.
- Integrate social authentication if desired.

---

For any issues, check Django documentation or reach out to the project maintainer.
