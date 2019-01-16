from django.contrib.auth import get_user_model
from rest_framework import serializers

CurrentUser = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentUser
        fields = ('id', 'email', 'username')
