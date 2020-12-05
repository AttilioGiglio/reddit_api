from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer

# Create your views here.
# generics.ListAPIView is going to list data very fast
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Before a save a post, It will relate the post with a user 
    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)

class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post= Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post :)')
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return  Response(status=status.HTTP_204_NO_CONTENT)
        else: 
            raise ValidationError('You never voted for this post... avispate!')