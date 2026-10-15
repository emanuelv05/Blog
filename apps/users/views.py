from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import CreateView, DetailView, UpdateView, View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .forms import UserForm, ProfileForm
from .models import User, Profile, Follow

# Create your views here.
# Registro de usuario
class SignupView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, "Usuario registrado exitosamente.")
        return redirect(self.success_url)

    def get_success_url(self):
        return reverse('user:profile', kwargs={'pk': self.object.pk})

# Inicio de sesion
class Signinview(View):
    def get(self, request):
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })

    def post(self, request):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return render(request, 'signin.html', {
                'form': AuthenticationForm
            })
        login(request, user)
        messages.success(self.request, "Inicio de sesion exitosamente.")
        return redirect('core:home')

# Cerrar sesion
class SignoutView(View):
    def post(self, request):
        logout(request)
        return redirect('core:home')

# Ver perfil
class ProfileView(DetailView):
    model = Profile
    template_name = 'user/profile.html'

# Actualizar perfil
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'user/update_profile.html'

    # Siempre devuelve el perfil del usuario autenticado, nunca el de otro
    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado correctamente")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user:profile', kwargs={'pk': self.request.user.pk})

# Seguidores/Seguidos
class UserFollowView(LoginRequiredMixin, View):
    def post(self, request, pk):
        target = get_object_or_404(User, pk=pk)
        follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            follow.delete()
            is_following = False
        else:
            is_following = True
        return JsonResponse({'success': True, 'following': is_following})


    


        


