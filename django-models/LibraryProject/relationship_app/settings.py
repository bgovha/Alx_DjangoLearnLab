import os

# Add to the existing settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'relationship_app/static'),
]