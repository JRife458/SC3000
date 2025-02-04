from django.urls import path
from .views import SummarizeGameView
from .views import speak_text
from .views import tts_test_page

app_name = "ai_sportcaster"

urlpatterns = [
    path('test/', SummarizeGameView.as_view(), name="test"),
    path('speak/', speak_text, name='speak_text'),
    path('tts-test/', tts_test_page, name='tts_test_page'),
]
