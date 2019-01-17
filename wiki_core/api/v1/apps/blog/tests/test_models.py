from django.contrib.auth.models import User
from django.test import TestCase

from api.v1.apps.blog import models


class PostTests(TestCase):
    fixtures = ['initial_data']

    def setUp(self):
        self.pk = 1
        self.p = models.Post.objects.get(pk=self.pk)

    def test_create_post(self):
        p = models.Post.objects.create(title='test_create')
        p.save()
        self.assertEqual(p.title, 'test_create')
        self.assertIsNotNone(p.pk)

    def test_get_post(self):
        self.assertEqual(self.p.pk, self.pk)

    def test_title(self):
        self.assertEqual(self.p.title, 'post 1')

    def test_str(self):
        self.assertEqual(str(self.p), self.p.title)

    def test_updated_property(self):
        edition = self.p.post_contents.filter(is_published=True).first()
        self.assertEqual(self.p.updated, edition.created)

        edition = self.p.post_contents.filter(is_published=False).first()
        edition.is_published = True
        edition.save()

        self.assertEqual(self.p.updated, edition.created)

    def test_editions_count_property(self):
        self.assertEqual(self.p.editions_count, self.p.post_contents.count())


class PostContentTests(TestCase):
    fixtures = ['initial_data']

    def setUp(self):
        self.pk = 4
        self.post_content = models.PostContent.objects.get(pk=self.pk)
        self.admin = User.objects.get(username='admin')

    def test_get_post_content(self):
        self.assertEqual(self.post_content.pk, self.pk)

    def test_content_text(self):
        self.assertEqual(self.post_content.text, 'post 1 edition 1')

    def test_str(self):
        self.assertEqual(str(self.post_content), '[2019-01-16 10:26:50.894000+00:00] <aa@aa.aa> post 1')

    def test_post_content_save(self):
        published_edition = self.post_content.post.post_contents.get(is_published=True)

        new_edition = models.PostContent.objects.create(
            text='test edition',
            author=self.admin,
            post=self.post_content.post
        )
        new_edition.save()

        self.assertEqual(self.post_content.post.post_contents.get(is_published=True).pk, new_edition.pk)
        self.assertNotEqual(published_edition.pk, new_edition.pk)

    def test_check_monkey_published(self):
        new_edition = None

        for i in range(20):
            new_edition = models.PostContent.objects.create(
                text='test edition %d' % i,
                author=self.admin,
                post=self.post_content.post
            )
            new_edition.save()

        self.assertEqual(self.post_content.post.post_contents.filter(is_published=True).count(), 1)
        self.assertEqual(self.post_content.post.post_contents.get(is_published=True), new_edition)



