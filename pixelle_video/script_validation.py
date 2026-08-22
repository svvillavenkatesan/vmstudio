"""Lightweight safety checks for AI-generated narration before rendering."""

from dataclasses import dataclass
from difflib import SequenceMatcher
import re


@dataclass(frozen=True)
class ScriptIssue:
    code: str
    severity: str
    scene_index: int | None = None


def _normalized(text: str) -> str:
    return re.sub(r"[^\w\u0B80-\u0BFF]+", " ", text.casefold()).strip()


def validate_script(
    topic: str,
    narrations: list[str],
    expected_scenes: int,
    output_language: str = "ta",
) -> list[ScriptIssue]:
    """Return deterministic warnings/errors that a creator can review."""
    issues: list[ScriptIssue] = []

    if len(narrations) != expected_scenes:
        issues.append(ScriptIssue("scene_count", "error"))

    normalized_topic = topic.casefold()
    normalized_scenes: list[str] = []
    for index, narration in enumerate(narrations):
        clean = narration.strip()
        normalized_scenes.append(_normalized(clean))
        if not clean:
            issues.append(ScriptIssue("empty_scene", "error", index))
            continue

        if output_language == "ta":
            tamil_chars = len(re.findall(r"[\u0B80-\u0BFF]", clean))
            latin_chars = len(re.findall(r"[A-Za-z]", clean))
            if tamil_chars == 0 or latin_chars > tamil_chars:
                issues.append(ScriptIssue("language_mismatch", "warning", index))

        if any(signal in normalized_topic for signal in ("பொங்கல்", "pongal")):
            if re.search(r"(?:தமிழர்|தமிழ்|பொங்கல்).{0,18}(?:மதம்|religion)", clean, re.IGNORECASE):
                issues.append(ScriptIssue("pongal_religion", "error", index))

        if any(signal in normalized_topic for signal in ("திருக்குறள்", "பாரதியார்", "thirukkural", "bharathiyar")):
            if any(mark in clean for mark in ('"', "“", "”", "‘", "’")):
                issues.append(ScriptIssue("unverified_quote", "warning", index))

    for left in range(len(normalized_scenes)):
        if not normalized_scenes[left]:
            continue
        for right in range(left + 1, len(normalized_scenes)):
            similarity = SequenceMatcher(None, normalized_scenes[left], normalized_scenes[right]).ratio()
            if similarity >= 0.72:
                issues.append(ScriptIssue("repeated_scene", "warning", right))
                break

    return issues


def has_blocking_issues(issues: list[ScriptIssue]) -> bool:
    return any(issue.severity == "error" for issue in issues)


def validate_visual_prompts(
    topic: str,
    prompts: list[str],
    expected_scenes: int,
) -> list[ScriptIssue]:
    """Check image prompts before they are sent to ComfyUI."""
    issues: list[ScriptIssue] = []
    if len(prompts) != expected_scenes:
        issues.append(ScriptIssue("visual_count", "error"))

    normalized_prompts: list[str] = []
    for index, prompt in enumerate(prompts):
        clean = prompt.strip()
        normalized_prompts.append(_normalized(clean))
        if not clean:
            issues.append(ScriptIssue("empty_visual", "error", index))
            continue

        tamil_chars = len(re.findall(r"[\u0B80-\u0BFF]", clean))
        if tamil_chars:
            issues.append(ScriptIssue("visual_not_english", "warning", index))

        positive_text_request = re.search(
            r"(?:readable|written|displaying|showing|include|with)\s+(?:Tamil\s+)?(?:text(?!-free)|letters|caption|title|logo|watermark|sign)",
            clean,
            re.IGNORECASE,
        )
        if positive_text_request:
            issues.append(ScriptIssue("embedded_text", "error", index))

        if any(signal in topic.casefold() for signal in ("சோழ", "சங்க", "chola", "sangam")):
            if re.search(r"\b(?:smartphone|car|skyscraper|electric light|television)\b", clean, re.IGNORECASE):
                issues.append(ScriptIssue("historical_mismatch", "error", index))

    for left in range(len(normalized_prompts)):
        if not normalized_prompts[left]:
            continue
        for right in range(left + 1, len(normalized_prompts)):
            if SequenceMatcher(None, normalized_prompts[left], normalized_prompts[right]).ratio() >= 0.78:
                issues.append(ScriptIssue("repeated_visual", "warning", right))
                break

    if any(signal in topic.casefold() for signal in ("பொங்கல்", "pongal")):
        combined = " ".join(prompts).casefold()
        anchors = sum(term in combined for term in ("kolam", "clay pot", "sugarcane", "turmeric"))
        if anchors < 2:
            issues.append(ScriptIssue("pongal_visual_context", "warning"))

    return issues
