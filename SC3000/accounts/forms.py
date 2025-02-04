from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Teams, Favorite_Teams, LanguagePreference

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
    CHOICES =(
    ("EN", "English"),
    ("JP", "Japanese"),
    ("SP", "Spanish")
)
    language = forms.ChoiceField(
        choices=CHOICES,
        required=True,

    )
    class Meta:
        model = Favorite_Teams
        fields = ['teams', 'language']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # language_preference = LanguagePreference.objects.get(user=user)

            # # Super hacky fix, creating a languagePreference object if none exists
            language_preference, created = LanguagePreference.objects.get_or_create(
            user=user,
            defaults={
                'language': 'EN',
            })
            self.fields['language'].initial = language_preference.language
            self.fields['teams'].initial = Favorite_Teams.objects.filter(user=user).values_list('team', flat=True)


    def save(self, user, commit=True):
        selected_teams = self.cleaned_data['teams']
        selected_language = self.cleaned_data['language']
        Favorite_Teams.objects.filter(user=user).delete()
        LanguagePreference.objects.filter(user=user).delete()
        LanguagePreference.objects.create(user=user, language=selected_language)
        Favorite_Teams.objects.bulk_create(
            [Favorite_Teams(user=user, team=team) for team in selected_teams]
        )
        return self.instance
