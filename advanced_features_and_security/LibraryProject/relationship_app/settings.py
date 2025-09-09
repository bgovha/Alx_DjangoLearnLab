import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add to the existing settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'relationship_app/static'),
]

AUTH_USER_MODEL = 'bookshelf.CustomUser'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')