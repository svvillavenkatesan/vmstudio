"""Private local character-reference storage for VMStudio."""

from __future__ import annotations

import io
import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from pixelle_video.utils.os_util import get_data_path


_ID = re.compile(r"^[a-f0-9]{32}$")
_MAX_IMAGE_BYTES = 10 * 1024 * 1024


def _root() -> Path:
    path = Path(get_data_path("characters")).resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def _paths(character_id: str) -> tuple[Path, Path]:
    if not _ID.fullmatch(character_id or ""):
        raise ValueError("Invalid character id")
    root = _root()
    metadata = (root / f"{character_id}.json").resolve()
    image = (root / f"{character_id}.png").resolve()
    if metadata.parent != root or image.parent != root:
        raise ValueError("Invalid character path")
    return metadata, image


def save_character(name: str, description: str, image_bytes: bytes, consent: bool) -> dict:
    """Validate, normalize and save an authorized reference image locally."""
    name = name.strip()[:80]
    description = description.strip()[:500]
    if not name or not description:
        raise ValueError("Name and appearance description are required")
    if not consent:
        raise ValueError("Consent confirmation is required")
    if not image_bytes or len(image_bytes) > _MAX_IMAGE_BYTES:
        raise ValueError("Reference image must be 10 MB or smaller")
    try:
        with Image.open(io.BytesIO(image_bytes)) as source:
            source.verify()
        with Image.open(io.BytesIO(image_bytes)) as source:
            normalized = source.convert("RGB")
            if normalized.width < 256 or normalized.height < 256:
                raise ValueError("Reference image must be at least 256×256")
            normalized.thumbnail((2048, 2048))
            character_id = uuid.uuid4().hex
            metadata_path, image_path = _paths(character_id)
            normalized.save(image_path, "PNG", optimize=True)
    except (UnidentifiedImageError, OSError) as error:
        raise ValueError("Unsupported or damaged reference image") from error
    item = {
        "id": character_id,
        "name": name,
        "description": description,
        "reference_path": str(image_path),
        "consent_confirmed": True,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    temporary = metadata_path.with_suffix(".tmp")
    temporary.write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporary, metadata_path)
    return item


def list_characters() -> list[dict]:
    items = []
    for metadata in _root().glob("*.json"):
        try:
            item = json.loads(metadata.read_text(encoding="utf-8"))
            _, image = _paths(item.get("id", ""))
            if image.exists() and item.get("consent_confirmed") is True:
                item["reference_path"] = str(image)
                items.append(item)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
    return sorted(items, key=lambda item: item.get("created_at", ""), reverse=True)


def delete_character(character_id: str) -> bool:
    metadata, image = _paths(character_id)
    existed = metadata.exists() or image.exists()
    metadata.unlink(missing_ok=True)
    image.unlink(missing_ok=True)
    return existed


def character_prompt(character: dict | None) -> str:
    if not character:
        return ""
    return (
        f"consistent recurring character named {character.get('name', '').strip()}, "
        f"appearance: {character.get('description', '').strip()}, preserve the same face, age, hairstyle and clothing across every scene"
    )
