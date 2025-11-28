def transcribe_audio_mock(audio_id: str) -> dict:
    """Mock transcription and translation."""
    mapping = {
        "audio_accident": {
            "text": "Accident hogaya, help bhejiye",
            "language": "hi",
            "translated_text": "There was an accident, send help",
            "urgency": "high"
        }
    }
    return mapping.get(audio_id, {"text":"Noisy background, worker at site", "language":"en", "translated_text":"Noisy background", "urgency":"low"})
