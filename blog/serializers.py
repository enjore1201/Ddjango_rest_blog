from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Blog, Comment

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id']


class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    comment_count = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    def get_comment_count(self, obj):
        return obj.comment_set.count()

    def get_author_name(self, obj):
        return obj.author.username



    class Meta:
        model = Blog
        fields = ['id', 'title', 'author', 'content', 'published_at', 'created_at', 'updated_at', 'comment_count', 'author_name']


class CommentSerializer(serializers.ModelSerializer):
    # blog = BlogSerializer(many=False, read_only=True)
    author = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'blog', 'author']

                            # CommentSerializer (author)상속을 받음
class CommentUpdateSerializer(CommentSerializer):
    # blog = BlogSerializer(many=False, read_only=True)
    # author = UserSerializer(many=False, read_only=True)
    blog = BlogSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'blog', 'author']