import os
from google.cloud import texttospeech
from django.conf import settings
from decouple import config

def text_to_speech(text: str, lang: str, output_filename="summary_audio.mp3") -> str:
    if config("ENVIRONMENT", default="prod") == 'dev':
        env_value = config("GOOGLE_APPLICATION_CREDENTIALS")
        os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", env_value)
        # print("Development mode: GOOGLE_APPLICATION_CREDENTIALS set to", os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
    # else:
        # print("Production mode: Using ADC provided by Cloud Run's service account.")

    # Print the values to see what's going on
    # print("Value from config('GOOGLE_APPLICATION_CREDENTIALS'):", env_value)
    # print("os.environ['GOOGLE_APPLICATION_CREDENTIALS']:", os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))


    """
    Generates an MP3 file from the given text using Google TTS.
    In local dev, it uses the JSON key if GOOGLE_APPLICATION_CREDENTIALS is set.
    In production (GAE), it uses the default service account ADC.
    """
    # 1. Create a client
    #    If GOOGLE_APPLICATION_CREDENTIALS is set, the library automatically uses it.
    #    Otherwise, on GAE, it uses the GAE service account credentials.
    client = texttospeech.TextToSpeechClient()

    # 2. Build the synthesis request
    synthesis_input = texttospeech.SynthesisInput(text=text)
    LANGUAGE_CODE_CHOICES = {
    "EN": "en-AU",
    "JP": "ja-JP",
    "SP": "es-US"
    }
    LANGUAGE_NAME_CHOICES = {
    "EN": "en-AU-Polyglot-1",
    "JP": "ja-JP-Neural2-D",
    "SP": "es-US-News-E"
    }
    voice = texttospeech.VoiceSelectionParams(
        language_code=LANGUAGE_CODE_CHOICES[lang.language],
        name=LANGUAGE_NAME_CHOICES[lang.language],
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # 3. Get the TTS response
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # 4. Build the absolute path to MEDIA_ROOT.
    file_path = os.path.join(settings.MEDIA_ROOT, output_filename)

    # Hacky fix for relative path issue
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # 5. Write the audio content to that path.
    with open(file_path, "wb") as out:
        out.write(response.audio_content)

    return output_filename
