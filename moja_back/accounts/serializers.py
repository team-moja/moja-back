from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User, UserRank

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

class UserRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRank
        fields = ('user_rank',)

class UserDetailSerializer(serializers.ModelSerializer):
    rank = UserRankSerializer()

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_superuser', 'first_name', 'last_name', 'is_staff', 'is_active', 'groups', 'user_permissions']

class UserListSerializer(serializers.ModelSerializer):
    rank = UserRankSerializer()
    
    class Meta:
        model = User
        fields = ('username', 'nickname', 'user_point', 'rank',)