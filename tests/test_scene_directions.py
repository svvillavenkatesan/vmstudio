from pixelle_video.scene_directions import (
    apply_scene_directions,
    build_direction_prompt,
    normalize_scene_direction,
)


def test_invalid_scene_direction_values_are_normalized():
    value = normalize_scene_direction({
        "emotion": "unknown", "shot": "bad", "camera": "bad",
        "motion_strength": 500, "action": " walk forward ",
    })
    assert value == {
        "action": "walk forward", "emotion": "natural", "shot": "medium",
        "camera": "dolly_in", "motion_strength": 100,
    }


def test_direction_prompt_contains_cinematic_controls():
    prompt = build_direction_prompt({
        "action": "opens a school book", "emotion": "happy", "shot": "close_up",
        "camera": "tracking", "motion_strength": 70,
    })
    assert "opens a school book" in prompt
    assert "joyful expression" in prompt
    assert "close-up" in prompt
    assert "tracking shot" in prompt
    assert "70 percent" in prompt


def test_scene_directions_are_applied_by_index():
    prompts = apply_scene_directions(
        ["first scene", "second scene"],
        [{"emotion": "serious"}, {"camera": "pan_right"}],
    )
    assert "focused serious expression" in prompts[0]
    assert "camera pan right" in prompts[1]
