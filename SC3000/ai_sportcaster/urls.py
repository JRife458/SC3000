from django.urls import path
from .views import SummarizeGameView

app_name = "ai_sportcaster"

urlpatterns = [
    path('test/', SummarizeGameView.as_view(), name="test")
]
