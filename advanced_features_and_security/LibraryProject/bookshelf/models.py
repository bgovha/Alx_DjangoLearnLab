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
def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"