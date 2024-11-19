from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
  nickname = serializers.CharField(required=True, max_length=255)

  def get_cleaned_data(self):
    return {
      'username': self.validated_data.get('username', ''),
      'password1': self.validated_data.get('password1', ''),
      'email': self.validated_data.get('email', ''),
      'nickname': self.validated_data.get('nickname', ''),
    }