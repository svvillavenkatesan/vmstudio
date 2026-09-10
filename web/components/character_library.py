"""Character library UI with consent-gated local reference storage."""

from __future__ import annotations

import streamlit as st

from pixelle_video.character_store import delete_character, list_characters, save_character
from web.i18n import tr


def render_character_library() -> dict | None:
    with st.expander(tr("character.title"), expanded=False):
        st.caption(tr("character.help"))
        characters = list_characters()
        if characters:
            by_id = {item["id"]: item for item in characters}
            options = [""] + list(by_id)
            selected_id = st.selectbox(
                tr("character.choose"), options,
                format_func=lambda item_id: tr("character.none") if not item_id else by_id[item_id]["name"],
                key="selected_character_id",
            )
            if selected_id:
                selected = by_id[selected_id]
                preview_col, detail_col = st.columns([1, 2])
                preview_col.image(selected["reference_path"], use_container_width=True)
                detail_col.caption(selected["description"])
                confirm = detail_col.checkbox(tr("character.delete_confirm"), key=f"character_delete_confirm_{selected_id}")
                if detail_col.button(tr("character.delete"), disabled=not confirm, key=f"character_delete_{selected_id}"):
                    delete_character(selected_id)
                    st.session_state.pop("selected_character_id", None)
                    st.rerun()
            else:
                selected = None
        else:
            st.caption(tr("character.empty"))
            selected = None

        st.markdown(f"**{tr('character.add')}**")
        name = st.text_input(tr("character.name"), key="character_new_name")
        description = st.text_area(tr("character.description"), height=90, key="character_new_description")
        upload = st.file_uploader(tr("character.image"), type=["png", "jpg", "jpeg", "webp"], key="character_new_image")
        consent = st.checkbox(tr("character.consent"), key="character_new_consent")
        if st.button(tr("character.save"), disabled=not (name and description and upload and consent), use_container_width=True):
            try:
                saved = save_character(name, description, upload.getvalue(), consent)
                st.session_state["selected_character_id"] = saved["id"]
                st.success(tr("character.saved"))
                st.rerun()
            except ValueError as error:
                st.error(tr("character.error", error=str(error)))
        return selected
