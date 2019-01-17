from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.v1.apps.blog.models import Post, PostContent
from api.v1.apps.user.serializers import AuthorSerializer


CurrentUser = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'text')

    def get_text(self, obj):
        current_edition = obj.post_contents.filter(is_published=True).first()
        if current_edition:
            return PostContentSerializer(current_edition, read_only=True).data.get('text', '')
        else:
            return ''


class PostCreateSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    author = serializers.PrimaryKeyRelatedField(queryset=CurrentUser.objects.all())

    class Meta:
        model = Post
        fields = ['title', 'text', 'author']


class PostLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title')


class PostDetailSerializer(serializers.ModelSerializer):
    content = PostSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content')


class PostContentEditSerializer(serializers.ModelSerializer):
    text = serializers.CharField()

    class Meta:
        model = PostContent
        fields = ('post', 'text', 'author')


class PostContentSerializer(serializers.ModelSerializer):

    post = PostLiteSerializer(read_only=True)
    text = serializers.CharField(read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = PostContent
        fields = ('id', 'post', 'text', 'author', 'created')
