from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api.v1.apps.blog.models import Post, PostContent
from api.v1.apps.blog.serializers import PostContentSerializer
from . import serializers


# TODO: add pagination, ordering, searching


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [AllowAny, ]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostSerializer
        if self.action == 'retrieve':
            if self.request.user and self.request.user.is_superuser:
                return serializers.PostSerializer
        return serializers.PostSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, ])
    def edit(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)

        data = {'text': request.POST.get('text'), 'post': post.pk, 'author': request.user.pk}
        print(data)
        print(request.POST)
        serializer = serializers.PostContentEditSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Your post edition was successfully saved'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['get'])
    # def get_versions(self, request, pk=None):
    #     post = get_object_or_404(Post, pk=pk)
    #     serializer = serializers.PostContentSerializer(post.post_contents, many=True)
    #     return Response(serializer.data)


class PostEditionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PostContent.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = PostContentSerializer

    def retrieve(self, request, pk=None, post_id=None):
        if pk == 'current':
            content = PostContent.objects.get(post__pk=post_id, is_published=True)
        else:
            queryset = self.get_queryset()
            content = get_object_or_404(queryset, pk=pk)
        serializer = PostContentSerializer(content)
        return Response(serializer.data)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        queryset = PostContent.objects.filter(post=post)
        return queryset

    @action(detail=True, methods=['get'], permission_classes=[IsAdminUser, ])
    def set_published(self, request, pk=None, *args, **kwargs):
        post_content = get_object_or_404(PostContent, pk=pk, post_id=kwargs.get('post_id'))
        if not post_content.is_published:
            post_content.is_published = True
            post_content.save()
        else:
            return Response({'detail': 'This post was already published'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'This post was successfully published'})
