from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import CustomUserCreationForm

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

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"
