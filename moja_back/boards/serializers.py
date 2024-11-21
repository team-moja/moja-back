from rest_framework import serializers
from .models import HelpArticle, HelpLike, HelpComment

################################################
# 질문
# 질문 게시판 글
class HelpArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpArticle
        fields = ['id', 'user', 'help_title', 'help_content', 'help_date', 'help_delete_date']
        read_only_fields = ['id', 'user', 'help_date']


# 질문 좋아요
class HelpLikeSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    
    class Meta:
        model = HelpLike
        fields = ['id', 'user', 'help_title', 'help_content', 'help_date', 'like_count']
        read_only_fields = ['id', 'user', 'help_date', 'like_count']

# 질문 댓글
class HelpCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpComment
        fields = ['id', 'user', 'help_article', 'help_comment_content', 'help_comment_date', 'help_comment_delete_date']
################################################