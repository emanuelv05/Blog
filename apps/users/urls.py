from django.urls import path
from .views import (SignupView,
                    Signinview,
                    SignoutView,
                    ProfileView,
                    ProfileUpdateView,
                    UserFollowView)

app_name = 'user'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', Signinview.as_view(), name='signin'),
    path('signout/', SignoutView.as_view(), name='signout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='update_profile'),
    path('follow/<int:pk>/', UserFollowView.as_view(), name='follow'),
]