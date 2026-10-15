from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import UpdateView, DeleteView
from apps.posts.models import Post
from .forms import CommentForm
from .models import Comment


# Crear comentario (o respuesta, si viene parent_id)
class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user

            # Validar que el parent (si existe) pertenezca al mismo post
            if comment.parent and comment.parent.post_id != post.pk:
                messages.error(request, "No se puede responder a un comentario de otro post.")
                return redirect('post:detail', pk=post.pk)

            # Evitar respuestas a respuestas (límite de un solo nivel)
            if comment.parent and comment.parent.parent_id is not None:
                messages.error(request, "No se puede responder a una respuesta.")
                return redirect('post:detail', pk=post.pk)

            comment.save()
            messages.success(request, "Comentario publicado.")
        else:
            messages.error(request, "No se pudo publicar el comentario.")

        return redirect('post:detail', pk=post.pk)


# Editar comentario (solo el dueño)
class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment/update.html'

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Comentario actualizado.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post:detail', kwargs={'pk': self.object.post.pk})


# Eliminar comentario (solo el dueño)
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment/delete_confirm.html'

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('post:detail', kwargs={'pk': self.object.post.pk})