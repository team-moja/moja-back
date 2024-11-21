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
        articles = HelpArticle.objects.all().order_by('-help_date')
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


# 질문 게시판 글 상세 조회, 수정 및 삭제
@api_view(['GET', 'PUT', 'DELETE'])
def help_article_detail(request, pk):
    article = get_object_or_404(HelpArticle, pk=pk)

    if request.method == 'GET':
        serializer = HelpArticleSerializer(article)
        data = serializer.data
        # 좋아요 수와 좋아요 상태 추가
        data['like_count'] = HelpLike.objects.filter(help_article=article).count()
        data['is_liked'] = HelpLike.objects.filter(
            help_article=article,
            user=request.user
        ).exists()
        return Response(data)
        # return Response(serializer.data)

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

    # 현재 사용자의 좋아요 상태 확인
    like = HelpLike.objects.filter(user=request.user, help_article=article)
    
    # 좋아요가 이미 있으면 삭제 (취소)
    if like.exists():
        like.delete()
        like_count = HelpLike.objects.filter(help_article=article).count()
        return Response({
            'like_count': like_count,
            'is_liked': False
        }, status=status.HTTP_200_OK)
    
    # 좋아요가 없으면 생성
    else:
        HelpLike.objects.create(user=request.user, help_article=article)
        like_count = HelpLike.objects.filter(help_article=article).count()
        return Response({
            'like_count': like_count,
            'is_liked': True
        }, status=status.HTTP_201_CREATED)


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