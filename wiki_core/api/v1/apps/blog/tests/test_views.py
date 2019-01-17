from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from api.v1.apps.blog.models import Post

admin_token = 'ee09cddebf71df4ebe5b6741197f081b4b0fb4ac'
user_token = '754bc683369a1f211bb8a91a76a07b861e2c7806'

anon_client = APIClient()
admin_client = APIClient()
user_client = APIClient()

admin_client.credentials(HTTP_AUTHORIZATION='Token ' + admin_token)
user_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)


class PostList(TestCase):
    fixtures = ['initial_data']

    def test_post_list(self):
        response = anon_client.get(
            reverse('v1_post-list'),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostGet(TestCase):
    fixtures = ['initial_data']

    def test_post_get(self):
        response = anon_client.get(
            reverse('v1_post-detail', kwargs={'pk': Post.objects.first().pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostCreate(TestCase):
    fixtures = ['initial_data']

    def test_post_create(self):
        response = user_client.post(
            reverse('v1_post-list'),
            data={'title': 'new-test-post', 'text': 'new-test-post-text'}
        )

        post = Post.objects.get(pk=response.json().get('id'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('new-test-post', response.json().get('title'))
        self.assertEqual(post.title, response.json().get('title'))
        self.assertEqual(post.post_contents.get(is_published=True).text, 'new-test-post-text')

    def test_post_edit(self):
        post = Post.objects.first()
        response = user_client.post(
            reverse('v1_post-edit', kwargs={'pk': post.id}),
            data={'text': 'test-post-edit-text'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.post_contents.get(is_published=True).text, 'test-post-edit-text')


class PostContentList(TestCase):
    fixtures = ['initial_data']

    def setUp(self):
        self.post = Post.objects.get(title='post 1')

    def test_post_list(self):
        response = anon_client.get(
            reverse('v1_post_edition-list', kwargs={'post_id': self.post.pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostContentGet(TestCase):
    fixtures = ['initial_data']

    def setUp(self):
        self.post = Post.objects.get(title='post 1')
        self.post_current = self.post.post_contents.get(is_published=True)

    def test_post_get(self):
        response = anon_client.get(
            reverse('v1_post_edition-detail', kwargs={'post_id': self.post.pk, 'pk': self.post_current.pk}),
        )
        obj = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.get('id'), self.post_current.pk)

    def test_post_get_current(self):
        response = anon_client.get(
            reverse('v1_post_edition-detail', kwargs={'post_id': self.post.pk, 'pk': 'current'}),
        )
        obj = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.get('id'), self.post_current.pk)


class PostContentSetPublished(TestCase):
    fixtures = ['initial_data']

    def setUp(self):
        self.post = Post.objects.get(title='post 1')
        self.post_current = self.post.post_contents.get(is_published=True)

    def test_post_content_set_published_anon(self):
        edition = self.post.post_contents.filter(is_published=False).first()
        response = anon_client.get(
            reverse('v1_post_edition-set-published', kwargs={'post_id': self.post.pk, 'pk': edition.pk}),
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.post.post_contents.get(is_published=True).pk, self.post_current.pk)

    def test_post_content_set_published_user(self):
        edition = self.post.post_contents.filter(is_published=False).first()
        response = user_client.get(
            reverse('v1_post_edition-set-published', kwargs={'post_id': self.post.pk, 'pk': edition.pk}),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.post.post_contents.get(is_published=True).pk, self.post_current.pk)

    def test_post_content_set_published_admin(self):
        edition = self.post.post_contents.filter(is_published=False).first()
        response = admin_client.get(
            reverse('v1_post_edition-set-published', kwargs={'post_id': self.post.pk, 'pk': edition.pk}),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.post_contents.get(is_published=True).pk, edition.pk)

    def test_post_content_set_published_that_was_already_published(self):
        response = admin_client.get(
            reverse('v1_post_edition-set-published', kwargs={'post_id': self.post.pk, 'pk': self.post_current.pk}),
        )

        obj = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(obj.get('detail'), 'This post was already published')
        self.assertEqual(self.post.post_contents.get(is_published=True).pk, self.post_current.pk)
