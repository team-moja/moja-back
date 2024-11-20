from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

from .serializers import UserDetailSerializer, UserListSerializer, UserModifySerializer
from .models import User


# Create your views here.
@api_view(['GET', 'PUT'])
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserModifySerializer(user, data = request.data, partial = True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

@api_view(['GET'])
def user_list(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserListSerializer(user, many = True)
        return Response(serializer.data)
    
# 마이페이지
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    serializer = UserDetailSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    
    if 'profile_image' in request.FILES:
        file = request.FILES['profile_image']
        file_name = f'profile_images/{user.username}/{file.name}'
        
        # 기존 이미지 삭제
        if user.profile_image:
            default_storage.delete(user.profile_image.path)
            
        # 새 이미지 저장
        path = default_storage.save(file_name, ContentFile(file.read()))
        user.profile_image = path

    serializer = UserDetailSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)