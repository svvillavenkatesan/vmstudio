"""Review/edit step between local AI script generation and video rendering."""

import hashlib
import json

import streamlit as st

from pixelle_video.script_validation import has_blocking_issues, validate_script
from pixelle_video.utils.content_generators import generate_narrations_from_topic
from web.i18n import tr
from web.utils.async_helpers import run_async
from web.components.project_drafts import autosave_draft


def _review_id(video_params: dict) -> str:
    source = {
        "text": video_params.get("text", ""),
        "n_scenes": video_params.get("n_scenes", 5),
        "output_language": video_params.get("output_language", "ta"),
        "content_mode": video_params.get("content_mode", "story"),
    }
    return hashlib.sha256(json.dumps(source, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:12]


def render_script_review(pixelle_video, video_params: dict) -> tuple[dict, bool]:
    """Render review controls and return fixed-script params when approved."""
    if video_params.get("mode", "generate") != "generate":
        return video_params, True

    review_id = _review_id(video_params)
    state_key = f"script_review_{review_id}"
    loaded = st.session_state.get("loaded_draft") or {}
    if state_key not in st.session_state and loaded.get("topic") == video_params.get("text") and loaded.get("narrations"):
        st.session_state[state_key] = loaded["narrations"]
        st.session_state[f"script_approved_{review_id}"] = bool(loaded.get("script_approved"))
        for index, narration in enumerate(loaded["narrations"]):
            st.session_state[f"script_scene_{review_id}_{index}"] = narration
    st.markdown(f"**{tr('script_review.title')}**")
    st.caption(tr("script_review.help"))

    if st.button(tr("script_review.generate"), key=f"generate_script_{review_id}", use_container_width=True):
        if not video_params.get("text", "").strip():
            st.error(tr("error.input_required"))
        else:
            try:
                with st.spinner(tr("script_review.generating")):
                    narrations = run_async(generate_narrations_from_topic(
                        pixelle_video.llm,
                        topic=video_params["text"],
                        n_scenes=video_params.get("n_scenes", 5),
                        min_words=video_params.get("min_narration_words", 8),
                        max_words=video_params.get("max_narration_words", 22),
                        output_language="Tamil" if video_params.get("output_language", "ta") == "ta" else "English",
                        content_mode=video_params.get("content_mode", "story"),
                    ))
                    st.session_state[state_key] = narrations
                    st.session_state[f"script_approved_{review_id}"] = False
                    for index, narration in enumerate(narrations):
                        st.session_state[f"script_scene_{review_id}_{index}"] = narration
            except Exception as error:
                st.error(tr("script_review.generation_failed", error=str(error)))

    stored = st.session_state.get(state_key)
    if not stored:
        st.info(tr("script_review.not_generated"))
        return video_params, False

    edited: list[str] = []
    for index, narration in enumerate(stored):
        edited.append(st.text_area(
            tr("script_review.scene", n=index + 1),
            value=narration,
            height=110,
            key=f"script_scene_{review_id}_{index}",
        ).strip())

    issues = validate_script(
        video_params.get("text", ""),
        edited,
        video_params.get("n_scenes", 5),
        video_params.get("output_language", "ta"),
    )
    for issue in issues:
        scene = "" if issue.scene_index is None else tr("script_review.scene_ref", n=issue.scene_index + 1)
        message = tr(f"script_review.issue.{issue.code}", scene=scene)
        st.error(message) if issue.severity == "error" else st.warning(message)

    approved = st.checkbox(
        tr("script_review.approve"),
        key=f"script_approved_{review_id}",
        disabled=has_blocking_issues(issues),
    )
    autosave_draft(video_params, narrations=edited, script_approved=approved)
    if not approved:
        st.caption(tr("script_review.approval_required"))
        return video_params, False

    reviewed_params = dict(video_params)
    reviewed_params.update({
        "mode": "fixed",
        "text": "\n\n".join(edited),
        "split_mode": "paragraph",
        "title": video_params.get("title") or video_params.get("text", "")[:60],
    })
    return reviewed_params, True
