from django.urls import path

from accounts.views import UserLoginView, UserSignupView, UserProfileView, TeamGamesView
from ai_sportcaster.views import SummarizeGameView
from .views import HomePageRedirectView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', HomePageRedirectView.as_view(), name="redirect"),
    path('login/', UserLoginView.as_view(next_page="profile"), name="login"),
    path('signup/', UserSignupView.as_view(), name="signup"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('logout/', LogoutView.as_view(next_page="login"), name="logout"),
    path('games/', TeamGamesView.as_view(), name="games"),
    path('test/', SummarizeGameView.as_view(), name="test")
]
