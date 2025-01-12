from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import MasterUser

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterUser
        fields = ['id', 'email', 'password', 'username']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MasterUser.objects.create_user(**validated_data)
        return user
