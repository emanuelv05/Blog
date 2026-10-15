from django.urls import path
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView

app_name = 'comment'

urlpatterns = [
    path('create/<int:pk>/', CommentCreateView.as_view(), name='create'),   # pk = id del post
    path('update/<int:pk>/', CommentUpdateView.as_view(), name='update'),   # pk = id del comentario
    path('delete/<int:pk>/', CommentDeleteView.as_view(), name='delete'),   # pk = id del comentario
]