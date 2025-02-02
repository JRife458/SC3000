from django.urls import path

from .views import UserLoginView, UserSignupView, UserProfileView, favorite_team_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="login"),
    path('signup/', UserSignupView.as_view(), name="signup"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('logout/', LogoutView.as_view(next_page="login"), name="logout"),
    path('favTeams/', favorite_team_view, name="post-fav-team")
]
