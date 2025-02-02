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
from .models import Favorite_Teams, Teams
import json

class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_field_name = "accounts/profile.html"
    def form_valid(self, form):
        messages.success(self.request, f"Welcome {self.request.user.username}!")
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
    success_url = reverse_lazy("profile")

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

# @csrf_exempt
# def favorite_team_view(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         print(data)
#         # new_teams = FavoriteTeams.objects.create(user_id=data["user_id"], teams=data["teams"])
#         return JsonResponse({"new_teams": "new_teams"})
#     else:
#         return JsonResponse({"message": "post-fave-teams"})
