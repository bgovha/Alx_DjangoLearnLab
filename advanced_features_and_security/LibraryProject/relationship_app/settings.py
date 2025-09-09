import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add to the existing settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'relationship_app/static'),
]

# Add to your existing settings
AUTH_USER_MODEL = 'relationship_app.CustomUser'  # Replace 'relationship_app' with your actual app name

# Add media settings for profile photos
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')