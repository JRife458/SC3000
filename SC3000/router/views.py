from django.shortcuts import render
from django.views.generic.base import RedirectView
from django.contrib.auth.models import User

# Create your views here.
class HomePageRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return '/profile/'
        return '/login/'
