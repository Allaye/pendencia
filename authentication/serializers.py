from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from authentication.models import User


class RegisterApiViewSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=125, min_length=5, write_only=True)


    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginApiViewSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ('email', 'password', 'token')

        read_only_fields = ['token']