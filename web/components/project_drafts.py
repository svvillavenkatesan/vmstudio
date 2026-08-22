"""Project draft controls and autosave helpers."""

from datetime import datetime

import streamlit as st

from pixelle_video.draft_store import delete_draft, list_drafts, load_draft, save_draft
from web.i18n import tr


_WIDGET_FIELDS = {
    "topic": "topic_text",
    "title": "video_title",
    "mode": "create_mode",
    "output_language": "output_language",
    "content_mode": "content_mode",
    "cultural_style": "cultural_style",
    "art_style": "art_style",
    "image_animation": "image_animation",
    "one_minute_mode": "one_minute_mode",
    "n_scenes": "n_scenes",
    "split_mode": "split_mode",
}


def _label(draft: dict) -> str:
    name = draft.get("title") or draft.get("topic") or tr("draft.untitled")
    raw = draft.get("updated_at", "")
    try:
        stamp = datetime.fromisoformat(raw).astimezone().strftime("%d-%m-%Y %I:%M %p")
    except ValueError:
        stamp = ""
    return f"{name[:42]} · {stamp}"


def render_project_drafts() -> None:
    drafts = list_drafts()
    with st.expander(tr("draft.title"), expanded=False):
        if not drafts:
            st.caption(tr("draft.empty"))
        else:
            by_id = {item["id"]: item for item in drafts}
            selected = st.selectbox(
                tr("draft.choose"), list(by_id), format_func=lambda item_id: _label(by_id[item_id]),
                key="draft_selector",
            )
            left, right = st.columns(2)
            if left.button(tr("draft.open"), use_container_width=True):
                draft = load_draft(selected)
                st.session_state["active_draft_id"] = selected
                st.session_state["loaded_draft"] = draft
                for field, widget_key in _WIDGET_FIELDS.items():
                    if field in draft:
                        st.session_state[widget_key] = draft[field]
                st.rerun()
            confirm = right.checkbox(tr("draft.delete_confirm"), key=f"delete_confirm_{selected}")
            if right.button(tr("draft.delete"), disabled=not confirm, use_container_width=True):
                delete_draft(selected)
                if st.session_state.get("active_draft_id") == selected:
                    st.session_state.pop("active_draft_id", None)
                    st.session_state.pop("loaded_draft", None)
                st.rerun()
        if st.button(tr("draft.new"), use_container_width=True):
            st.session_state.pop("active_draft_id", None)
            st.session_state.pop("loaded_draft", None)
            for widget_key in _WIDGET_FIELDS.values():
                st.session_state.pop(widget_key, None)
            st.rerun()


def autosave_draft(video_params: dict, **review_values) -> dict | None:
    topic = video_params.get("text", "").strip()
    if not topic:
        return None
    values = {
        "topic": topic,
        "title": video_params.get("title", ""),
        "mode": video_params.get("mode", "generate"),
        "output_language": video_params.get("output_language", "ta"),
        "content_mode": video_params.get("content_mode", "story"),
        "cultural_style": video_params.get("cultural_style", "auto"),
        "art_style": video_params.get("art_style", "auto"),
        "image_animation": video_params.get("image_animation", "none"),
        "one_minute_mode": video_params.get("one_minute_mode", False),
        "n_scenes": video_params.get("n_scenes", 5),
        "split_mode": video_params.get("split_mode", "paragraph"),
        **review_values,
    }
    draft = save_draft(values, st.session_state.get("active_draft_id"))
    st.session_state["active_draft_id"] = draft["id"]
    st.session_state["loaded_draft"] = draft
    return draft
