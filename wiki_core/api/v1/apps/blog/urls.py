from django.urls import path

from rest_framework.routers import DefaultRouter

from api.v1.apps.blog.views import PostViewSet, PostEditionViewSet

router = DefaultRouter()
router.register(r'post/(?P<post_id>.+)/edition', PostEditionViewSet, basename='v1_post_edition')
router.register(r'post', PostViewSet, basename='v1_post')


urlpatterns = router.urls
