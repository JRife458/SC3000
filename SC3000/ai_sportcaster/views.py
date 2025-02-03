from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .summarize_layer import get_gemini_summary

@require_POST
def summarize_game(request):
    """
    This view receives a POST request with a 'prompt',
    calls the Gemini AI summarization service, and returns the result.
    """
    # Retrieve the prompt from the POST data. If none is provided, use a default.
    prompt = request.POST.get("prompt", "Explain how AI works")

    try:
        # Call our service to get the summary from Gemini AI
        summary = get_gemini_summary(prompt)
        # Return the summary as a JSON response
        return JsonResponse({"summary": summary})
    except Exception as e:
        # Return an error message if something goes wrong
        return JsonResponse({"error": str(e)}, status=500)

def test_page(request):
    return render(request, 'ai_sportcaster/test_ai.html')
