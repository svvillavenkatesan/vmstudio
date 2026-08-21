"""Subtitle controls for the final video composition layer."""

import streamlit as st

from web.i18n import tr


def render_subtitle_config() -> dict:
    with st.container(border=True):
        st.markdown(f"**{tr('subtitle.title')}**")
        enabled = st.toggle(tr("subtitle.enabled"), value=True)
        if not enabled:
            return {"enabled": False, "mode": "off"}

        mode = st.selectbox(
            tr("subtitle.mode"),
            ["standard", "karaoke", "bilingual"],
            format_func=lambda value: tr(f"subtitle.mode.{value}"),
        )
        font = st.selectbox(
            tr("subtitle.font"),
            ["Noto Sans Tamil", "Noto Serif Tamil", "Nirmala UI", "Latha"],
        )
        size = st.slider(tr("subtitle.size"), 28, 84, 52, 2)
        col1, col2 = st.columns(2)
        with col1:
            color = st.color_picker(tr("subtitle.color"), "#FFFFFF")
        with col2:
            highlight_color = st.color_picker(tr("subtitle.highlight_color"), "#FFD54F")
        position = st.selectbox(
            tr("subtitle.position"),
            ["bottom", "middle", "top"],
            format_func=lambda value: tr(f"subtitle.position.{value}"),
        )
        safe_zone = st.toggle(tr("subtitle.safe_zone"), value=True)
        st.caption(tr("subtitle.composition_help"))
        return {
            "enabled": True,
            "mode": mode,
            "font": font,
            "size": size,
            "color": color,
            "highlight_color": highlight_color,
            "position": position,
            "safe_zone": safe_zone,
        }
