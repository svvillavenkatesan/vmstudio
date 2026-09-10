import io

import pytest
from PIL import Image

from pixelle_video.character_store import character_prompt, delete_character, list_characters, save_character


def _image_bytes(size=(512, 512)):
    stream = io.BytesIO()
    Image.new("RGB", size, (120, 80, 60)).save(stream, "JPEG")
    return stream.getvalue()


def test_character_requires_consent(monkeypatch, tmp_path):
    monkeypatch.setenv("PIXELLE_VIDEO_ROOT", str(tmp_path))
    with pytest.raises(ValueError, match="Consent"):
        save_character("Arun", "Tamil school student", _image_bytes(), False)


def test_character_round_trip_and_delete(monkeypatch, tmp_path):
    monkeypatch.setenv("PIXELLE_VIDEO_ROOT", str(tmp_path))
    saved = save_character("Arun", "Tamil school student with short black hair", _image_bytes(), True)
    assert saved["consent_confirmed"] is True
    assert list_characters()[0]["name"] == "Arun"
    assert "preserve the same face" in character_prompt(saved)
    assert delete_character(saved["id"]) is True
    assert list_characters() == []


def test_character_rejects_tiny_image(monkeypatch, tmp_path):
    monkeypatch.setenv("PIXELLE_VIDEO_ROOT", str(tmp_path))
    with pytest.raises(ValueError, match="256"):
        save_character("Arun", "Description", _image_bytes((128, 128)), True)
