import os
import google.generativeai as genai
from decouple import config  # Import config from decouple

def get_gemini_summary(prompt: str) -> str:
    """
    This function configures the Gemini AI model using your API key,
    sends a prompt to generate content, and returns the summary text.
    """
    # Retrieve the API key from environment variables
    api_key = config("GEMINI_KEY")
    if not api_key:
        raise ValueError("Gemini API key is not set in environment variables.")

    # Configure the gemini API with the API key
    genai.configure(api_key=api_key)

    # Initialize the model (this might change depending on your specific Gemini model name)
    # model = genai.GenerativeModel("gemini-1.5-flash")
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
    system_instruction="Act as a sportscaster. I'm going to send a string of data from MLB games. Summarize it as excited as possible. This is the game object game_obj = {'home': {},'away': {},'plays': [],'score': {'home': '','away': '',}}",
    )

    # Generate content from the prompt
    response = model.generate_content(prompt)

    print(response)
    # Return the generated summary text
    return response.text
