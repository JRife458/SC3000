from django.urls import path

from .views import UserLoginView, UserSignupView, UserProfileView, TeamGamesView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="login"),
    path('signup/', UserSignupView.as_view(), name="signup"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('logout/', LogoutView.as_view(next_page="login"), name="logout"),
    path('games/', TeamGamesView.as_view(), name="games")
]
