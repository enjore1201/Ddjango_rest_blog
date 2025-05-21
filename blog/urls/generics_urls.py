from django.urls import path, include
from django.views import generic

from blog.views import generics_views as views

app_name = "generics_api"



urlpatterns = [

    path('blog', views.BlogListAPIView.as_view(), name='blog_list'),
    path('blog/<int:pk>', views.RetrieveUpdateDestroyAPIView.as_view(), name='blog_detail'),
    path('blog/<int:blog_pk>/comment', views.CommentListCreateAPIView.as_view(), name='comment_list_create'),
    path('comment/<int:pk>', views.CommentUpdateDestroyAPIView.as_view(), name='comment_update_delete'),
]
