from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Post

# Formulario para el crud de post
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tag', 'category', 'image']

    # Validar el titulo del post
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("El titulo del post no puede tener espacios vacios.")
        if len(title) < 3:
            raise ValidationError("El titulo del post debe tener al menos 3 caracteres.")
        return title


