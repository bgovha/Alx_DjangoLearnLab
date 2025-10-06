
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment

class BlogCRUDTests(TestCase):
    """Placeholder for Blog CRUD test cases."""
    pass

class CommentSystemTests(TestCase):
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
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            status='published'
        )

    def test_comment_creation(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('blog:add_comment', args=[self.post.pk]), {
            'content': 'This is a test comment.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Comment.objects.filter(content='This is a test comment.').exists())

    def test_comment_edit_author(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Original comment'
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('blog:edit_comment', args=[comment.pk]), {
            'content': 'Updated comment content'
        })
        self.assertEqual(response.status_code, 302)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated comment content')

    def test_comment_edit_non_author(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Original comment'
        )
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('blog:edit_comment', args=[comment.pk]))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_comment_deletion(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Comment to delete'
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('blog:delete_comment', args=[comment.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_comment_like_functionality(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('blog:comment_like_toggle', args=[comment.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(comment.user_has_liked(self.user))

    def test_comment_reply(self):
        parent_comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Parent comment'
        )
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.post(reverse('blog:add_comment_reply', args=[self.post.pk, parent_comment.pk]), {
            'content': 'This is a reply'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(parent=parent_comment, content='This is a reply').exists())

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