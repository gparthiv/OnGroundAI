def transcribe_audio_mock(audio_id: str) -> dict:
    """Mock transcription + translation with urgency detection."""

    mapping = {
        "audio_accident": {
            "text": "Accident hogaya, help bhejiye",
            "language": "hi",
            "translated_text": "There was an accident, send help",
            "urgency": "high"
        },
        "audio_lowbattery": {
            "text": "Battery low, may not be able to update",
            "language": "en",
            "translated_text": "Battery low, updating may stop",
            "urgency": "medium"
        },
        "audio_minoraccident": {
            "text": "Slip hogaya, minor accident but I'm fine",
            "language": "hi",
            "translated_text": "I slipped, minor accident but I'm fine",
            "urgency": "medium"
        },
        "audio_confusion": {
            "text": "Yahan ka address alag lag raha hai",
            "language": "hi",
            "translated_text": "The address here looks different",
            "urgency": "low"
        },
        "audio_angrycustomer": {
            "text": "Customer bahut gussa hai",
            "language": "hi",
            "translated_text": "Customer is very angry",
            "urgency": "medium"
        },
        "audio_sirenbackground": {
            "text": "Hearing loud sirens nearby",
            "language": "en",
            "translated_text": "Hearing loud sirens",
            "urgency": "medium"
        },
        "audio_shock_urgent": {
            "text": "Zor ka jhatka laga, help!",
            "language": "hi",
            "translated_text": "A strong electric shock hit me, help!",
            "urgency": "high"
        },
        "audio_noisyworksite": {
            "text": "Too much noise at site",
            "language": "en",
            "translated_text": "The site is very noisy",
            "urgency": "low"
        },
        "audio_heavybreathing": {
            "text": "Breathing heavily... need... break...",
            "language": "en",
            "translated_text": "Breathing heavily, need break",
            "urgency": "medium"
        }
    }

    return mapping.get(audio_id, {
        "text": "Unclear audio",
        "language": "en",
        "translated_text": "Unclear audio",
        "urgency": "low"
    })
