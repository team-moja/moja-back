from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
  nickname = serializers.CharField(required=True, max_length=255)
  birth_date = serializers.DateField()
  user_monthly_income = serializers.IntegerField()
  user_monthly_expenses = serializers.IntegerField()

  def get_cleaned_data(self):
    return {
      'username': self.validated_data.get('username', ''),
      'password1': self.validated_data.get('password1', ''),
      'nickname': self.validated_data.get('nickname', ''),
      'email': self.validated_data.get('email', ''),
      'birth_date': self.validated_data.get('birth_date', ''),
      'user_monthly_income': self.validated_data.get('user_monthly_income', ''),
      'user_monthly_expenses': self.validated_data.get('user_monthly_expenses', ''),
    }