from django.views.generic import ListView
from apps.posts.models import Post


class HomeView(ListView):
    model = Post
    template_name = 'core/home.html'
    context_object_name = 'posts'
    paginate_by = 10  # paginación nativa de Django, sin lógica extra

    def get_queryset(self):
        return Post.objects.select_related('user', 'category').prefetch_related('tag')