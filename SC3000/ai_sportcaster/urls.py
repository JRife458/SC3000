from django.urls import path
from .views import summarize_game, test_page, SummarizeGameView

urlpatterns = [
    path('summarize/', summarize_game, name='summarize_game'),
    path('test/', test_page, name='test_page'),
    path('test2/', SummarizeGameView.as_view(), name="test2")
]
