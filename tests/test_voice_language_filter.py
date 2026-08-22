from pixelle_video.tts_voices import get_preview_text, get_voices_for_output_language


def test_tamil_video_only_offers_tamil_voices():
    voices = get_voices_for_output_language("ta")
    assert {voice["id"] for voice in voices} == {
        "ta-IN-PallaviNeural", "ta-IN-ValluvarNeural"
    }


def test_english_video_only_offers_english_voices():
    voices = get_voices_for_output_language("en")
    assert voices
    assert all(voice["locale"].startswith("en-") for voice in voices)


def test_preview_text_matches_video_language():
    assert "வணக்கம்" in get_preview_text("ta")
    assert get_preview_text("en").startswith("Hello")
