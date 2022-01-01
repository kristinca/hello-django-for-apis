from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post


class BlogTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create a user
        testuser1 = User.objects.create_user(
            username='testuserNo1', password='thepass123'
        )
        testuser1.save()

        # create a blog post
        test_post = Post.objects.create(
            author=testuser1, title='Blog title', body='Some content')
        test_post.save()

    def test_blog_content(self):
        post = Post.objects.get(id=1)
        author = f'{post.author}'
        title = f'{post.title}'
        body = f'{post.body}'
        self.assertEqual(author, 'testuserNo1')
        self.assertEqual(title, 'Blog title')
        self.assertEqual(body, 'Some content')
