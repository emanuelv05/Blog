from django.db import models
from apps.users.models import User

# Create your models here.
# Modelo categoria
class Category(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.title

# Modelo etiquetas
class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.title

# Modelo post
class Post(models.Model):
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(max_length=10000, blank=False)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='id_category')
    user = models.ForeignKey(User, on_delete=models.PROTECT, db_column='id_user')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"




