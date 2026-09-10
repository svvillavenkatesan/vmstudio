"""Validated scene direction presets shared by the UI and video pipeline."""

from __future__ import annotations

from typing import Any


EMOTIONS = {
    "natural": "natural calm expression",
    "happy": "warm joyful expression",
    "sad": "subtle sad expression",
    "angry": "controlled angry expression",
    "surprised": "natural surprised expression",
    "hopeful": "hopeful confident expression",
    "excited": "energetic excited expression",
    "serious": "focused serious expression",
}

SHOTS = {
    "close_up": "cinematic close-up shot",
    "medium": "cinematic medium shot",
    "wide": "cinematic wide shot",
    "full_body": "full-body cinematic shot",
}

CAMERA_MOVES = {
    "static": "locked camera",
    "dolly_in": "slow dolly-in camera movement",
    "dolly_out": "slow dolly-out camera movement",
    "pan_left": "slow camera pan left",
    "pan_right": "slow camera pan right",
    "tracking": "smooth cinematic tracking shot",
    "handheld": "subtle controlled handheld camera movement",
}

ACTIONS = {
    "natural": "subtle natural breathing and blinking",
    "blink": "natural eye blinking with tiny head movement",
    "nod": "gently nodding while maintaining eye contact",
    "smile": "a gradual natural smile with subtle facial movement",
    "hand_gesture": "a calm explanatory hand gesture",
    "speaking": "natural speaking expression with restrained head and hand movement",
    "walking": "walking slowly with realistic full-body movement",
}


def normalize_scene_direction(value: dict[str, Any] | None) -> dict[str, Any]:
    """Return a safe, stable scene-direction dictionary."""
    value = value or {}
    emotion = value.get("emotion", "natural")
    shot = value.get("shot", "medium")
    camera = value.get("camera", "dolly_in")
    action_preset = value.get("action_preset", "natural")
    try:
        strength = int(value.get("motion_strength", 50))
    except (TypeError, ValueError):
        strength = 50
    return {
        "action": str(value.get("action", "")).strip()[:240],
        "action_preset": action_preset if action_preset in ACTIONS else "natural",
        "emotion": emotion if emotion in EMOTIONS else "natural",
        "shot": shot if shot in SHOTS else "medium",
        "camera": camera if camera in CAMERA_MOVES else "dolly_in",
        "motion_strength": max(0, min(100, strength)),
    }


def build_direction_prompt(value: dict[str, Any] | None) -> str:
    """Convert one scene direction into a text-free English visual instruction."""
    direction = normalize_scene_direction(value)
    parts = [SHOTS[direction["shot"]], EMOTIONS[direction["emotion"]]]
    parts.append(ACTIONS[direction["action_preset"]])
    if direction["action"]:
        parts.append(f"character action: {direction['action']}")
    if direction["camera"] != "static":
        parts.append(CAMERA_MOVES[direction["camera"]])
    parts.append(f"motion intensity {direction['motion_strength']} percent")
    return ", ".join(parts)


def apply_scene_directions(
    prompts: list[str | None], directions: list[dict[str, Any]] | None
) -> list[str | None]:
    """Append matching cinematic directions to generated media prompts."""
    if not directions:
        return prompts
    enhanced: list[str | None] = []
    for index, prompt in enumerate(prompts):
        if prompt is None or index >= len(directions):
            enhanced.append(prompt)
            continue
        enhanced.append(f"{prompt}, {build_direction_prompt(directions[index])}")
    return enhanced
