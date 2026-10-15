from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from apps.posts.models import Post
from apps.comments.models import Comment
from .models import Like


# Like/unlike a un post
class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, comment=None, user=request.user)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({
            'success': True,
            'liked': liked,
            'total_likes': post.likes.count(),
        })


# Like/unlike a un comentario
class CommentLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        like, created = Like.objects.get_or_create(post=None, comment=comment, user=request.user)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({
            'success': True,
            'liked': liked,
            'total_likes': comment.likes.count(),
        })