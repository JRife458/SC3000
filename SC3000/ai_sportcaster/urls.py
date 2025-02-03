from django.urls import path
from .views import summarize_game, test_page

urlpatterns = [
    path('summarize/', summarize_game, name='summarize_game'),
    path('test/', test_page, name='test_page'),
]
