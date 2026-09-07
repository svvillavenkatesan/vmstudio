# Copyright (C) 2025 AIDC-AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Guided three-step creator UI for the standard VMStudio pipeline."""

import streamlit as st
from typing import Any
from web.i18n import tr

from web.pipelines.base import PipelineUI, register_pipeline_ui

# Import components
from web.components.content_input import render_content_input, render_bgm_section, render_version_info
from web.components.style_config import render_style_config
from web.components.output_preview import render_output_preview
from web.components.project_drafts import autosave_draft, render_project_drafts


class StandardPipelineUI(PipelineUI):
    """
    UI for the Standard Video Generation Pipeline.
    Keeps all existing controls and generation parameters, but presents them as
    a simple creator journey instead of a dense multi-column technical form.
    """
    name = "quick_create"
    icon = "⚡"
    
    @property
    def display_name(self):
        return tr("pipeline.quick_create.name")
    
    @property
    def description(self):
        return tr("pipeline.quick_create.description")
    
    def render(self, pixelle_video: Any):
        render_project_drafts()

        create_tab, design_tab, generate_tab = st.tabs(
            [
                "① உள்ளடக்கம்",
                "② குரல் & தோற்றம்",
                "③ சரிபார்த்து உருவாக்கு",
            ]
        )

        # All tabs are evaluated by Streamlit, so parameters remain available
        # for final generation while only the active stage is visible.
        with create_tab:
            with st.container(key="vm_content_panel"):
                st.caption("தலைப்பு, மொழி, உள்ளடக்க வகை மற்றும் வீடியோ நீளத்தைத் தேர்வு செய்யுங்கள்.")
                # Content input (mode, text, title, n_scenes)
                content_params = render_content_input()

                # BGM selection (bgm_path, bgm_volume)
                bgm_params = render_bgm_section()

        with design_tab:
            with st.container(key="vm_design_panel"):
                st.caption("குரல், காட்சி பாணி, திரை விகிதம் மற்றும் subtitle அமைப்புகளைத் தேர்வு செய்யுங்கள்.")
                # Style configuration (TTS, template, workflow, etc.)
                style_params = render_style_config(pixelle_video)

        with generate_tab:
            with st.container(key="vm_generate_panel"):
                st.caption("AI ஸ்கிரிப்டைச் சரிபார்த்து இறுதி வீடியோவை உருவாக்குங்கள்.")
                # Combine all parameters
                video_params = {
                    "pipeline": self.name,
                    **content_params,
                    **bgm_params,
                    **style_params
                }
                if not video_params.get("batch_mode"):
                    autosave_draft(video_params)

                # Render output preview (generate button, progress, video preview)
                render_output_preview(pixelle_video, video_params)

                with st.expander("VMStudio பதிப்பு விவரம்", expanded=False):
                    render_version_info()


# Register self
register_pipeline_ui(StandardPipelineUI)
