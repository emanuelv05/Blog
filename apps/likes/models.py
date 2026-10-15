from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from apps.posts.models import Post
from apps.comments.models import Comment

# Create your models here.
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='likes', db_column='id_post')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='likes', db_column='id_comment')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes', db_column='id_user')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], condition=models.Q(post__isnull=False), name='unique_like_post'),
            models.UniqueConstraint(fields=['comment', 'user'], condition=models.Q(comment__isnull=False), name='unique_like_comment'),
        ]

    def clean(self):
        if bool(self.post) == bool(self.comment):
            raise ValidationError("El like debe pertenecer a un post O a un comentario, no ambos ni ninguno.")

    def __str__(self):
        target = self.post or self.comment
        return f"{self.user.username} le dio like a {target}"
