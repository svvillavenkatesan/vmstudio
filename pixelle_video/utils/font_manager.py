"""Bundled Tamil font registry and CSS embedding helpers."""

import base64
from functools import lru_cache
from pathlib import Path


FONT_OPTIONS = {
    "Noto Sans Tamil": {
        "file": "assets/fonts/noto_sans_tamil/NotoSansTamil-Variable.ttf",
        "fallback": "'Nirmala UI', 'Latha', sans-serif",
        "bundled": True,
    },
    "Noto Serif Tamil": {
        "file": "assets/fonts/noto_serif_tamil/NotoSerifTamil-Variable.ttf",
        "fallback": "'Nirmala UI', 'Latha', serif",
        "bundled": True,
    },
    "Nirmala UI": {"file": None, "fallback": "'Latha', sans-serif", "bundled": False},
    "Latha": {"file": None, "fallback": "'Nirmala UI', sans-serif", "bundled": False},
}


def normalize_font_name(font: str | None) -> str:
    return font if font in FONT_OPTIONS else "Noto Sans Tamil"


def font_family_css(font: str | None) -> str:
    name = normalize_font_name(font)
    return f"'{name}', {FONT_OPTIONS[name]['fallback']}"


@lru_cache(maxsize=1)
def bundled_font_face_css() -> str:
    """Return self-contained font faces so rendering never needs an installed font."""
    root = Path(__file__).resolve().parents[2]
    rules = []
    for name, config in FONT_OPTIONS.items():
        relative_file = config.get("file")
        if not relative_file:
            continue
        font_path = root / relative_file
        if not font_path.exists():
            continue
        encoded = base64.b64encode(font_path.read_bytes()).decode("ascii")
        rules.append(
            "@font-face {"
            f"font-family: '{name}';"
            f"src: url(data:font/ttf;base64,{encoded}) format('truetype');"
            "font-style: normal;font-weight: 100 900;font-display: block;"
            "}"
        )
    return "\n".join(rules)
