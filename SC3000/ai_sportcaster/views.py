from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .summarize_layer import get_gemini_summary
from accounts.models import Favorite_Teams, Teams, LanguagePreference
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
import statsapi
from .voice_layer import text_to_speech
from django.conf import settings               # <-- import settings

# @require_POST
# def summarize_game(request):
#     """
#     This view receives a POST request with a 'prompt',
#     calls the Gemini AI summarization service, and returns the result.
#     """
#     # Retrieve the prompt from the POST data. If none is provided, use a default.
#     prompt = request.POST.get("prompt", "Explain how AI works")

#     try:
#         # Call our service to get the summary from Gemini AI
#         summary = get_gemini_summary(prompt)
#         # Return the summary as a JSON response
#         return JsonResponse({"summary": summary})
#     except Exception as e:
#         # Return an error message if something goes wrong
#         return JsonResponse({"error": str(e)}, status=500)

# def test_page(request):
#     return render(request, 'ai_sportcaster/test_ai.html')

class SummarizeGameView(LoginRequiredMixin, TemplateView):
    template_name = "ai_sportcaster/test_ai.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        fav_teams = Favorite_Teams.objects.filter(user_id=user.id)
        context["favorite_teams"] = fav_teams
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
        language_pref = LanguagePreference.objects.get(user=user)
        summary = get_gemini_summary(f"{games}", language_pref)
        context["summary"] = summary
        filename = text_to_speech(summary, output_filename="summary_audio.mp3")
        audio_url = f"{settings.MEDIA_URL}{filename}"
        context["audio"] = audio_url

        return context

@require_POST
def speak_text(request):
    """
    Accepts a POST request with 'text' parameter,
    calls text_to_speech to generate an MP3, and returns the file path (or direct file).
    """
    # 1. Get the text to speak from the POST data
    text = request.POST.get("text", "Hello, this is a default message.")

    # 2. Generate the MP3 file
    filename = text_to_speech(text, output_filename="summary_audio.mp3")

    audio_url = f"{settings.MEDIA_URL}{filename}"

    # 3. Return a JSON response with the filename OR
    #    return the file itself. Let's do a JSON response for now.
    return JsonResponse({
        "message": "Text-to-speech completed",
        # "filename": filename
        "audio_url": audio_url
    })

def tts_test_page(request):
    return render(request, 'ai_sportcaster/tts_test.html')
