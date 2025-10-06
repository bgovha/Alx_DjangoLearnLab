from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MinLengthValidator
import uuid

class Tag(models.Model):
    name = models.CharField(
        max_length=50, 
        unique=True,
        validators=[MinLengthValidator(2)]
    )
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(max_length=200, blank=True)
    color = models.CharField(max_length=7, default='#6c757d')  # Hex color code
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    post_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:posts_by_tag', kwargs={'tag_slug': self.slug})
    
    def update_post_count(self):
        """Update the post count for this tag"""
        self.post_count = self.posts.count()
        self.save(update_fields=['post_count'])
    
    @property
    def is_popular(self):
        """Check if tag is popular (more than 5 posts)"""
        return self.post_count > 5

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, help_text="Brief description of the post")
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    view_count = models.PositiveIntegerField(default=0)
    search_vector = models.SearchVectorField(null=True, blank=True)  # For full-text search
    
    class Meta:
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure slug is unique
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        if not self.excerpt and self.content:
            self.excerpt = self.content[:297] + "..." if len(self.content) > 300 else self.content
            
        super().save(*args, **kwargs)
        
        # Update tag counts
        for tag in self.tags.all():
            tag.update_post_count()
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})
    
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    @property
    def is_published(self):
        return self.status == 'published' and self.published_date <= timezone.now()
    
    def get_related_posts(self):
        """Get posts with similar tags"""
        return Post.objects.filter(
            tags__in=self.tags.all(),
            status='published',
            published_date__lte=timezone.now()
        ).exclude(id=self.id).distinct()[:4]

# Signal to update tag counts when posts are saved
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

@receiver(m2m_changed, sender=Post.tags.through)
def update_tag_count(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        for tag in instance.tags.all():
            tag.update_post_count()

class Comment(models.Model):
    post = models.ForeignKey(
        'Post', 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    likes = models.ManyToManyField(
        User, 
        related_name='comment_likes', 
        blank=True
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['approved']),
        ]
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post.pk}) + f'#comment-{self.pk}'
    
    @property
    def is_reply(self):
        """Check if this comment is a reply to another comment"""
        return self.parent is not None
    
    @property
    def reply_count(self):
        """Get the number of replies to this comment"""
        return self.replies.count()
    
    @property
    def like_count(self):
        """Get the number of likes for this comment"""
        return self.likes.count()
    
    def user_has_liked(self, user):
        """Check if a user has liked this comment"""
        return self.likes.filter(id=user.id).exists()
    
    def can_edit(self, user):
        """Check if user can edit this comment"""
        return user == self.author or user.is_staff
    
    def can_delete(self, user):
        """Check if user can delete this comment"""
        return user == self.author or user == self.post.author or user.is_staff