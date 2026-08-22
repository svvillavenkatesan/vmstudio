"""Local, secret-free project draft storage for VMStudio."""

from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pixelle_video.utils.os_util import get_data_path


_ID_PATTERN = re.compile(r"^[a-f0-9]{32}$")
_ALLOWED_FIELDS = {
    "id", "topic", "title", "mode", "output_language", "content_mode",
    "cultural_style", "n_scenes", "split_mode", "narrations",
    "image_prompts", "script_approved", "visual_approved", "updated_at",
}


def _draft_dir() -> Path:
    path = Path(get_data_path("drafts")).resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def _draft_path(draft_id: str) -> Path:
    if not _ID_PATTERN.fullmatch(draft_id or ""):
        raise ValueError("Invalid draft id")
    path = (_draft_dir() / f"{draft_id}.json").resolve()
    if path.parent != _draft_dir():
        raise ValueError("Invalid draft path")
    return path


def save_draft(values: dict[str, Any], draft_id: str | None = None) -> dict[str, Any]:
    """Create or update a draft, retaining only explicitly safe fields."""
    draft_id = draft_id or uuid.uuid4().hex
    destination = _draft_path(draft_id)
    previous = load_draft(draft_id) if destination.exists() else {}
    draft = {key: value for key, value in previous.items() if key in _ALLOWED_FIELDS}
    draft.update({key: value for key, value in values.items() if key in _ALLOWED_FIELDS})
    draft["id"] = draft_id
    draft["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    temporary = destination.with_suffix(".tmp")
    temporary.write_text(json.dumps(draft, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporary, destination)
    return draft


def load_draft(draft_id: str) -> dict[str, Any]:
    return json.loads(_draft_path(draft_id).read_text(encoding="utf-8"))


def list_drafts() -> list[dict[str, Any]]:
    drafts = []
    for path in _draft_dir().glob("*.json"):
        try:
            draft = json.loads(path.read_text(encoding="utf-8"))
            if draft.get("id") and _ID_PATTERN.fullmatch(draft["id"]):
                drafts.append(draft)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
    return sorted(drafts, key=lambda item: item.get("updated_at", ""), reverse=True)


def delete_draft(draft_id: str) -> bool:
    path = _draft_path(draft_id)
    if not path.exists():
        return False
    path.unlink()
    return True
