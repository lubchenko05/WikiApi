from django.test import TestCase

from api.v1.apps.blog.models import Post, PostContent


class PostTests(TestCase):
    fixtures = ['initial_data']

    def test_simple_test(self):
        s = Post.objects.get(pk=1)
        self.assertEqual(s.title, 'post 1')
