from django.urls import path, include

from rest_framework.authtoken import views as token_views


urlpatterns = [
    path('auth/', token_views.obtain_auth_token, name='v1_token_auth'),
    path('', include('api.v1.apps.blog.urls'))
]
