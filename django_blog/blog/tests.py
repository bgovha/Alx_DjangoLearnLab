# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Tag

class BlogCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        self.tag = Tag.objects.create(name='Django')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user,
            status='published'
        )
        self.post.tags.add(self.tag)

    def test_post_list_view(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_create_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'New Test Post',
            'content': 'This is a new test post content.',
            'status': 'published',
            'tags': [self.tag.pk]
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Post.objects.filter(title='New Test Post').exists())

    def test_post_create_view_unauthenticated(self):
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_post_update_view_author(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('blog:post_update', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_post_update_view_non_author(self):
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('blog:post_update', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_post_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('blog:post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request for deletion
        response = self.client.post(reverse('blog:post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())