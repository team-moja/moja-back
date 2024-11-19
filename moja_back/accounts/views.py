from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404

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
    