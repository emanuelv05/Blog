from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .forms import PostForm
from .models import Post

# Create your views here.

# Listar los post
class PostListView(ListView):
    model = Post
    template_name = 'post/list.html'
    context_object_name = 'posts'

# Crear un post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Post creado exitosamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post:detail', kwargs={'pk': self.object.pk})

# Detalle de un post
class PostDetailView(DetailView):
    model = Post
    template_name = 'post/detail.html'

# Actualizar un post
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/update.html'

    # Solo permite editar posts propios
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Post actualizado exitosamente")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post:detail', kwargs={'pk': self.object.pk})

# Eliminar post
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/delete_confirm.html'
    success_url = reverse_lazy('post:list')

    # Solo permite editar posts propios
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


