from django.db import models
from django.conf import settings
from apps.posts.models import Post

# Create your models here.
# Modelo comentario
class Comment(models.Model):
    content = models.TextField(max_length=1000, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', db_column='id_post')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', db_column='id_user')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} comentó en {self.post.title}"