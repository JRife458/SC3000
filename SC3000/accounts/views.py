from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm, FavoriteTeamsForm
from .models import Favorite_Teams, Teams, LanguagePreference
from ai_sportcaster.voice_layer import text_to_speech
from ai_sportcaster.summarize_layer import get_gemini_summary
from django.conf import settings
import json
import requests
import statsapi

class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    success_url = reverse_lazy("profile")
    def form_valid(self, form):
        user = form.get_user()
        messages.success(self.request, f"Welcome {user.username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

class UserSignupView(CreateView):
    template_name = "accounts/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")  # Redirect to login after successful signup

    def form_valid(self, form):
        messages.success(self.request, "Your account has been created! You can now log in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error creating account. Please check the form.")
        return super().form_invalid(form)

class UserProfileView(LoginRequiredMixin, FormView):
    template_name = "accounts/profile.html"
    queryset = Favorite_Teams.objects.all()
    form_class = FavoriteTeamsForm
    success_url = reverse_lazy("games")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["favorite_teams"] = Favorite_Teams.objects.filter(user_id=user.id)
        return context

    def get_form_kwargs(self):
        """Pass the logged-in user to the form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Ensure the user is assigned when saving."""
        form.save(user=self.request.user)
        messages.success(self.request, "Favorite Teams Successfully Saved.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error saving teams. Please check the form.")
        return super().form_invalid(form)

class TeamGamesView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/games.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        fav_teams = Favorite_Teams.objects.filter(user_id=user.id)
        if not fav_teams:
            fav_teams = [Favorite_Teams.objects.create(user_id=user.id, team_id=1)]
        context["favorite_teams"] = fav_teams
        language_pref = LanguagePreference.objects.get(user_id=user.id)
        # if not language_pref:
        #     language_pref = LanguagePreference.objects.create(user_id=user.id, language="EN")
        game_data = []
        for team in fav_teams:
            team_obj = Teams.objects.get(id=team.team_id)
            game_id = statsapi.last_game(team_obj.mlb_id)
            highlight_data = statsapi.game_scoring_play_data(game_id)
            game_data.append(highlight_data)
        games = []
        for game in game_data:
            game_obj = {
                "home": game["home"],
                "away": game["away"],
                "plays": [],
                "score": {
                    "home": "",
                    "away": "",
                }
            }
            highlights= []
            plays = game["plays"]
            for events in plays:
                result = events["result"]
                highlights.append(result)
            if highlights:
                last_score = highlights[-1]
                score = game_obj["score"]
                score["home"] = last_score["homeScore"]
                score["away"] = last_score["awayScore"]
            else:
                score["home"] = 0
                score["away"] = 0
                highlights.append({"description":"Game cancelled.", "homeScore": 0, "awayScore": 0})
            game_obj["plays"] = highlights
            games.append(game_obj)
        context["games"] = games
        summary = get_gemini_summary(f"{games}", language_pref, user.first_name)
        context["summary"] = summary
        filename = text_to_speech(summary, output_filename="summary_audio.mp3")
        audio_url = f"{settings.MEDIA_URL}{filename}"
        context["audio"] = audio_url
        return context
