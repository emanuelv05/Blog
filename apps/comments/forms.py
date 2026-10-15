from django import forms
from django.core.exceptions import ValidationError
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        # se llena desde el botón "responder" en el template
        widgets = {'parent': forms.HiddenInput()}

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise ValidationError("El comentario no puede estar vacío.")
        if len(content) < 2:
            raise ValidationError("El comentario es demasiado corto.")
        return content