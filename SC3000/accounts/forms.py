from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Teams, Favorite_Teams

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=60)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

class FavoriteTeamsForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Teams.objects.all(),
        required=True
    )
    class Meta:
        model = Favorite_Teams
        fields = ['teams']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['teams'].initial = Favorite_Teams.objects.filter(user=user).values_list('team', flat=True)


    def save(self, user, commit=True):
        selected_teams = self.cleaned_data['teams']
        print("here")
        Favorite_Teams.objects.filter(user=user).delete()
        Favorite_Teams.objects.bulk_create(
            [Favorite_Teams(user=user, team=team) for team in selected_teams]
        )
        return self.instance
