from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Modelo user
class User(AbstractUser):
    pass

# Modelo Perfil
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

# Modelo de seguidores y seguidos
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} sigue a {self.following}"

