from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import HelpArticle, HelpLike, HelpComment
from .serializers import HelpArticleSerializer, HelpLikeSerializer, HelpCommentSerializer
from accounts.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

################################################
# 질문 게시판
# 질문 게시판 글 리스트 및 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def help_article_list(request):
    if request.method == 'GET':
        articles = HelpArticle.objects.all()
        serializer = HelpArticleSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = HelpArticleSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)  # admin_user 대신 실제 인증된 사용자 사용
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
# def help_article_list(request):
#     if request.method == 'GET':
#         articles = HelpArticle.objects.all()
#         serializer = HelpArticleSerializer(articles, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = HelpArticleSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             print("유효성 검사 통과")
#             # serializer.save(user=request.user)
#             admin_user = User.objects.filter(username="admin").first()
#             serializer.save(user=admin_user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         print("유효성 검사 실패", serializer.data)


# 질문 게시판 글 상세 조회, 수정 및 삭제
@api_view(['GET', 'PUT', 'DELETE'])
def help_article_detail(request, pk):
    article = get_object_or_404(HelpArticle, pk=pk)

    if request.method == 'GET':
        serializer = HelpArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = HelpArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        article.delete()
        return Response({'message': f'질문 {article.help_title}이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


# 좋아요 추가 및 제거
@api_view(['POST', 'DELETE'])
def help_like_toggle(request, pk):
    article = get_object_or_404(HelpArticle, pk=pk)

    if request.method == 'POST':
        if HelpLike.objects.filter(user=request.user, help_article=article).exists():
            return Response({'message': '이미 좋아요를 누르셨습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        HelpLike.objects.create(user=request.user, help_article=article)
        return Response({'message': '좋아요가 추가되었습니다.'}, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        like = HelpLike.objects.filter(user=request.user, help_article=article).first()
        if like:
            like.delete()
            return Response({'message': '좋아요가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': '좋아요가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)


# 댓글 리스트 및 생성
@api_view(['GET', 'POST'])
def help_comment_list_create(request, pk=None):
    if request.method == 'GET':
        comments = HelpComment.objects.filter(help_article_id=pk)
        serializer = HelpCommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        article = get_object_or_404(HelpArticle, pk=pk)
        serializer = HelpCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, help_article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 댓글 상세 조회, 수정 및 삭제
@api_view(['GET', 'PUT', 'DELETE'])
def help_comment_detail(request, pk):
    comment = get_object_or_404(HelpComment, pk=pk)

    if request.method == 'GET':
        serializer = HelpCommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = HelpCommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response({'message': f'댓글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
################################################