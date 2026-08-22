import json

import pytest

from pixelle_video import draft_store


@pytest.fixture
def draft_directory(tmp_path, monkeypatch):
    monkeypatch.setattr(draft_store, "get_data_path", lambda *parts: str(tmp_path.joinpath(*parts)))
    return tmp_path / "drafts"


def test_draft_round_trip_and_update(draft_directory):
    first = draft_store.save_draft({"topic": "தமிழர் பாரம்பரியத்தில் பொங்கல்", "n_scenes": 5})
    updated = draft_store.save_draft({"title": "பொங்கல்"}, first["id"])

    assert updated["topic"] == "தமிழர் பாரம்பரியத்தில் பொங்கல்"
    assert updated["title"] == "பொங்கல்"
    assert draft_store.load_draft(first["id"])["n_scenes"] == 5
    assert draft_store.list_drafts()[0]["id"] == first["id"]


def test_draft_never_serializes_secrets(draft_directory):
    draft = draft_store.save_draft({
        "topic": "சோதனை",
        "api_key": "do-not-save",
        "comfyui_url": "private-address",
        "config": {"token": "secret"},
    })
    raw = (draft_directory / f"{draft['id']}.json").read_text(encoding="utf-8")

    assert "do-not-save" not in raw
    assert "private-address" not in raw
    assert "secret" not in raw


def test_invalid_id_is_rejected_and_delete_is_exact(draft_directory):
    draft = draft_store.save_draft({"topic": "test"})
    with pytest.raises(ValueError):
        draft_store.load_draft("../config")
    assert draft_store.delete_draft(draft["id"]) is True
    assert draft_store.delete_draft(draft["id"]) is False
