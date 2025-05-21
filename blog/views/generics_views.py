from django.utils import timezone

from django.db.models import Q
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from blog.models import Blog, Comment
from blog.serializers import BlogSerializer, CommentSerializer, CommentUpdateSerializer
from utils.models import TimestampModel
from utils.permissions import IsAuthorOrReadOnly


class BlogQuerSetMixin:
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(
            Q(published_at__isnull=True) |  ## 1. published_at 필드가 비어 있거나 (isnull=True)
            Q(published_at__gte=timezone.now())  # 2. published_at이 현재 시각 이후인 경우 (예약된 게시글)
        ).order_by('-created_at').select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogListAPIView(BlogQuerSetMixin, ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RetrieveUpdateDestroyAPIView(BlogQuerSetMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # def perform_update(self, serializer):
    #     serializer.save(author=self.request.user)


class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        blog = self.get_blog_object()
        serializer.save(author=self.request.user, blog=blog)

    def get_queryset(self):
        queryset = super().get_queryset()
        blog = self.get_blog_object()
        return queryset.filter(blog=blog)


    def get_blog_object(self):
        return get_object_or_404(Blog, pk=self.kwargs['blog_pk'])




class CommentUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    permission_classes = [IsAuthorOrReadOnly]



