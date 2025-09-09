from django.db import models

class Book(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Book Title",
        help_text="Enter the title of the book"
    )
    author = models.CharField(
        max_length=100,
        verbose_name="Author Name",
        help_text="Enter the author's full name"
    )
    publication_year = models.IntegerField(
        verbose_name="Publication Year",
        help_text="Enter the year the book was published"
    )
    use_in_migrations = True

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)