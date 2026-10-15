from django.urls import path
from .views import PostLikeView, CommentLikeView

app_name = 'like'

urlpatterns = [
    path('post/<int:pk>/', PostLikeView.as_view(), name='post_like'),
    path('comment/<int:pk>/', CommentLikeView.as_view(), name='comment_like'),
]