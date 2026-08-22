"""Review step for AI image prompts before local ComfyUI generation."""

import hashlib
import json

import streamlit as st

from pixelle_video.script_validation import has_blocking_issues, validate_visual_prompts
from pixelle_video.utils.content_generators import generate_image_prompts
from pixelle_video.utils.template_util import get_template_type
from web.i18n import tr
from web.utils.async_helpers import run_async
from web.components.project_drafts import autosave_draft


def _visual_review_id(video_params: dict, narrations: list[str]) -> str:
    source = {
        "topic": video_params.get("title", ""),
        "narrations": narrations,
        "template": video_params.get("frame_template", ""),
        "prompt_prefix": video_params.get("prompt_prefix", ""),
    }
    return hashlib.sha256(json.dumps(source, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:12]


def render_image_prompt_review(pixelle_video, video_params: dict, script_ready: bool) -> tuple[dict, bool]:
    """Return params containing approved image_prompts for image templates."""
    template = video_params.get("frame_template") or "1080x1920/default.html"
    if get_template_type(template) != "image":
        return video_params, True
    if not script_ready:
        return video_params, False

    narrations = [part.strip() for part in video_params.get("text", "").split("\n\n") if part.strip()]
    review_id = _visual_review_id(video_params, narrations)
    state_key = f"visual_review_{review_id}"
    loaded = st.session_state.get("loaded_draft") or {}
    if state_key not in st.session_state and loaded.get("image_prompts"):
        st.session_state[state_key] = loaded["image_prompts"]
        st.session_state[f"visual_approved_{review_id}"] = bool(loaded.get("visual_approved"))
        for index, prompt in enumerate(loaded["image_prompts"]):
            st.session_state[f"visual_prompt_{review_id}_{index}"] = prompt

    st.markdown(f"**{tr('visual_review.title')}**")
    st.caption(tr("visual_review.help"))
    if st.button(tr("visual_review.generate"), key=f"generate_visuals_{review_id}", use_container_width=True):
        try:
            with st.spinner(tr("visual_review.generating")):
                prompts = run_async(generate_image_prompts(
                    pixelle_video.llm,
                    narrations=narrations,
                    min_words=24,
                    max_words=55,
                ))
                st.session_state[state_key] = prompts
                st.session_state[f"visual_approved_{review_id}"] = False
                for index, prompt in enumerate(prompts):
                    st.session_state[f"visual_prompt_{review_id}_{index}"] = prompt
        except Exception as error:
            st.error(tr("visual_review.generation_failed", error=str(error)))

    stored = st.session_state.get(state_key)
    if not stored:
        st.info(tr("visual_review.not_generated"))
        return video_params, False

    edited: list[str] = []
    for index, prompt in enumerate(stored):
        edited.append(st.text_area(
            tr("visual_review.scene", n=index + 1),
            value=prompt,
            height=140,
            key=f"visual_prompt_{review_id}_{index}",
        ).strip())

    issues = validate_visual_prompts(
        video_params.get("title") or video_params.get("text", ""),
        edited,
        len(narrations),
    )
    for issue in issues:
        scene = "" if issue.scene_index is None else tr("script_review.scene_ref", n=issue.scene_index + 1)
        message = tr(f"visual_review.issue.{issue.code}", scene=scene)
        st.error(message) if issue.severity == "error" else st.warning(message)

    approved = st.checkbox(
        tr("visual_review.approve"),
        key=f"visual_approved_{review_id}",
        disabled=has_blocking_issues(issues),
    )
    autosave_draft(
        video_params,
        narrations=narrations,
        script_approved=True,
        image_prompts=edited,
        visual_approved=approved,
    )
    if not approved:
        st.caption(tr("visual_review.approval_required"))
        return video_params, False

    reviewed_params = dict(video_params)
    reviewed_params["image_prompts"] = edited
    return reviewed_params, True
