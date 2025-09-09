from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book

class Command(BaseCommand):
    help = 'Assign custom permissions to user groups'

    def handle(self, *args, **options):
        # Get content type for Book model
        content_type = ContentType.objects.get_for_model(Book)
        
        # Get or create groups
        admin_group, created = Group.objects.get_or_create(name='Admins')
        librarian_group, created = Group.objects.get_or_create(name='Librarians')
        member_group, created = Group.objects.get_or_create(name='Members')
        
        # Get all Book permissions
        book_permissions = Permission.objects.filter(content_type=content_type)
        
        # Assign permissions to groups
        # Admins get all permissions
        for perm in book_permissions:
            admin_group.permissions.add(perm)
        
        # Librarians can add, change, and view books
        librarian_perms = book_permissions.exclude(codename='can_delete_book')
        for perm in librarian_perms:
            librarian_group.permissions.add(perm)
        
        # Members can only view books
        view_perm = book_permissions.get(codename='can_view_book')
        member_group.permissions.add(view_perm)
        
        self.stdout.write(self.style.SUCCESS('Successfully assigned permissions to groups'))