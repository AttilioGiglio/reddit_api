from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer

# Create your views here.
# generics.ListAPIView is going to list data very fast
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Before a save a post, It will relate the post with a user 
    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)