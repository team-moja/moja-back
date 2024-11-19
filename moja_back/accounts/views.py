from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import UserDetailSerializer, UserListSerializer
from .models import User


# Create your views here.
@api_view(['GET'])
def user_detail(request, pk):
    if request.method == 'GET':
        user = User.objects.get(pk = pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    
@api_view(['GET'])
def user_list(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserListSerializer(user, many = True)
        return Response(serializer.data)
    