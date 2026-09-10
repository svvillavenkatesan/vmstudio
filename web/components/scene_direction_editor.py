"""Compact scene-by-scene direction editor for cinematic generation."""

from __future__ import annotations

import streamlit as st

from pixelle_video.scene_directions import (
    CAMERA_MOVES,
    EMOTIONS,
    SHOTS,
    ACTIONS,
    build_direction_prompt,
    normalize_scene_direction,
)
from pixelle_video.utils.prompt_helper import build_image_prompt
from pixelle_video.utils.template_util import get_template_type
from web.components.project_drafts import autosave_draft
from web.i18n import get_language, tr
from web.utils.async_helpers import run_async


_TA = {
    "natural": "இயல்பு", "happy": "மகிழ்ச்சி", "sad": "சோகம்", "angry": "கோபம்",
    "surprised": "ஆச்சரியம்", "hopeful": "நம்பிக்கை", "excited": "உற்சாகம்", "serious": "தீவிரம்",
    "close_up": "முக அருகுக் காட்சி", "medium": "நடுத்தரக் காட்சி", "wide": "அகலக் காட்சி",
    "full_body": "முழு உடல் காட்சி", "static": "நிலையான கேமரா", "dolly_in": "மெதுவாக அருகில்",
    "dolly_out": "மெதுவாக விலகுதல்", "pan_left": "இடப்புறம் நகர்தல்", "pan_right": "வலப்புறம் நகர்தல்",
    "tracking": "பின்தொடரும் கேமரா", "handheld": "மென்மையான கை கேமரா",
    "blink": "இயல்பாகக் கண் சிமிட்டுதல்", "nod": "மெதுவாகத் தலை அசைத்தல்",
    "smile": "இயல்பாகப் புன்னகைத்தல்", "hand_gesture": "விளக்கும் கை அசைவு",
    "speaking": "பேசும் இயல்பான அசைவு", "walking": "மெதுவாக நடத்தல்",
}


def _label(value: str) -> str:
    return _TA.get(value, value.replace("_", " ").title()) if get_language() == "ta_IN" else value.replace("_", " ").title()


def render_scene_direction_editor(pixelle_video, video_params: dict, ready: bool) -> tuple[dict, bool]:
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
            action_preset = st.selectbox(
                tr("scene_direction.action_preset"), list(ACTIONS),
                index=list(ACTIONS).index(current["action_preset"]),
                format_func=_label, key=f"scene_action_preset_{index}",
            )
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
            directions.append(normalize_scene_direction({"action": action, "action_preset": action_preset,
                                                         "emotion": emotion, "shot": shot,
                                                         "camera": camera, "motion_strength": strength}))
    updated = dict(video_params)
    updated["scene_directions"] = directions
    autosave_draft(updated, scene_directions=directions)
    _render_scene_preview(pixelle_video, updated, prompts, directions)
    return updated, True


def _render_scene_preview(
    pixelle_video,
    video_params: dict,
    prompts: list[str],
    directions: list[dict],
) -> None:
    """Generate only one selected scene before the expensive full render."""
    if not prompts:
        return

    with st.expander(tr("scene_preview.title"), expanded=False):
        st.caption(tr("scene_preview.help"))
        selected = st.selectbox(
            tr("scene_preview.select"),
            list(range(len(prompts))),
            format_func=lambda index: tr("scene_direction.scene", n=index + 1),
            key="scene_preview_selected",
        )
        workflow = video_params.get("media_workflow")
        reference = video_params.get("character_reference")
        media_type = get_template_type(video_params.get("frame_template") or "")
        media_type = media_type if media_type in {"image", "video"} else "image"
        state_key = f"scene_preview_result_{selected}"

        button_label = (
            tr("scene_preview.retry")
            if st.session_state.get(state_key)
            else tr("scene_preview.generate")
        )
        if st.button(button_label, key=f"scene_preview_button_{selected}", use_container_width=True):
            if not workflow:
                st.error(tr("scene_preview.workflow_required"))
            elif any(marker in workflow.lower() for marker in ("ipadapter", "animatediff_i2v")) and not reference:
                st.error(tr("character.reference_required"))
            else:
                prompt = build_image_prompt(prompts[selected], video_params.get("prompt_prefix", ""))
                prompt = f"{prompt}, {build_direction_prompt(directions[selected])}"
                params = {
                    "prompt": prompt,
                    "workflow": workflow,
                    "media_type": media_type,
                    "width": video_params.get("media_width"),
                    "height": video_params.get("media_height"),
                    "duration": 1 if media_type == "video" else None,
                }
                if reference:
                    params["reference_image"] = str(reference)
                try:
                    with st.spinner(tr("scene_preview.generating")):
                        result = run_async(pixelle_video.media(**params))
                    st.session_state[state_key] = result.url
                    st.session_state[f"scene_preview_approved_{selected}"] = False
                except Exception as error:
                    st.error(tr("scene_preview.failed", error=str(error)))

        preview_path = st.session_state.get(state_key)
        if preview_path:
            if media_type == "video":
                st.video(preview_path)
            else:
                st.image(preview_path, use_container_width=True)
            st.checkbox(
                tr("scene_preview.approve"),
                key=f"scene_preview_approved_{selected}",
            )
