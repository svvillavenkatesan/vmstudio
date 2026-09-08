"""Compact scene-by-scene direction editor for cinematic generation."""

from __future__ import annotations

import streamlit as st

from pixelle_video.scene_directions import CAMERA_MOVES, EMOTIONS, SHOTS, normalize_scene_direction
from web.components.project_drafts import autosave_draft
from web.i18n import get_language, tr


_TA = {
    "natural": "இயல்பு", "happy": "மகிழ்ச்சி", "sad": "சோகம்", "angry": "கோபம்",
    "surprised": "ஆச்சரியம்", "hopeful": "நம்பிக்கை", "excited": "உற்சாகம்", "serious": "தீவிரம்",
    "close_up": "முக அருகுக் காட்சி", "medium": "நடுத்தரக் காட்சி", "wide": "அகலக் காட்சி",
    "full_body": "முழு உடல் காட்சி", "static": "நிலையான கேமரா", "dolly_in": "மெதுவாக அருகில்",
    "dolly_out": "மெதுவாக விலகுதல்", "pan_left": "இடப்புறம் நகர்தல்", "pan_right": "வலப்புறம் நகர்தல்",
    "tracking": "பின்தொடரும் கேமரா", "handheld": "மென்மையான கை கேமரா",
}


def _label(value: str) -> str:
    return _TA.get(value, value.replace("_", " ").title()) if get_language() == "ta_IN" else value.replace("_", " ").title()


def render_scene_direction_editor(video_params: dict, ready: bool) -> tuple[dict, bool]:
    if not ready:
        return video_params, False
    prompts = video_params.get("image_prompts") or []
    if not prompts:
        return video_params, True
    existing = video_params.get("scene_directions") or []
    directions = []
    with st.expander(tr("scene_direction.title"), expanded=False):
        st.caption(tr("scene_direction.help"))
        for index in range(len(prompts)):
            current = normalize_scene_direction(existing[index] if index < len(existing) else None)
            st.markdown(f"**{tr('scene_direction.scene', n=index + 1)}**")
            action = st.text_input(
                tr("scene_direction.action"), value=current["action"],
                placeholder=tr("scene_direction.action_placeholder"), key=f"scene_action_{index}",
            )
            emotion_col, shot_col, camera_col = st.columns(3)
            with emotion_col:
                emotion = st.selectbox(tr("scene_direction.emotion"), list(EMOTIONS),
                    index=list(EMOTIONS).index(current["emotion"]), format_func=_label, key=f"scene_emotion_{index}")
            with shot_col:
                shot = st.selectbox(tr("scene_direction.shot"), list(SHOTS),
                    index=list(SHOTS).index(current["shot"]), format_func=_label, key=f"scene_shot_{index}")
            with camera_col:
                camera = st.selectbox(tr("scene_direction.camera"), list(CAMERA_MOVES),
                    index=list(CAMERA_MOVES).index(current["camera"]), format_func=_label, key=f"scene_camera_{index}")
            strength = st.slider(tr("scene_direction.strength"), 0, 100, current["motion_strength"], 10,
                key=f"scene_strength_{index}")
            directions.append(normalize_scene_direction({"action": action, "emotion": emotion, "shot": shot,
                                                         "camera": camera, "motion_strength": strength}))
    updated = dict(video_params)
    updated["scene_directions"] = directions
    autosave_draft(updated, scene_directions=directions)
    return updated, True
