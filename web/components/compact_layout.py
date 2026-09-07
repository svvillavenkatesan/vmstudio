"""Compact desktop workspace styling for VMStudio."""

import streamlit as st


def render_studio_stepbar() -> None:
    """Render the compact creation path used by the desktop studio shell."""
    st.markdown(
        """
        <div class="vm-workflow-strip" aria-label="வீடியோ உருவாக்கும் வழிகாட்டி">
          <div class="vm-workflow-title">வீடியோ உருவாக்க வழிகாட்டி</div>
          <div class="vm-workflow-steps">
            <span class="vm-workflow-step is-active"><b>1</b> உள்ளடக்கம்</span>
            <span class="vm-workflow-line"></span>
            <span class="vm-workflow-step"><b>2</b> குரல் &amp; வடிவம்</span>
            <span class="vm-workflow-line"></span>
            <span class="vm-workflow-step"><b>3</b> முன்னோட்டம்</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_compact_desktop_layout() -> None:
    """Fit the studio shell within one desktop viewport.

    Long forms remain usable through independent column scrolling, while the
    browser page itself stays stable and the three main stages remain visible.
    """
    st.markdown(
        """
        <style>
        :root { --vm-panel-height: calc(100vh - 300px); }

        /* VMStudio dark creative-suite palette. */
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background:
                radial-gradient(circle at 82% 8%, rgba(43, 112, 255, .18), transparent 26%),
                radial-gradient(circle at 12% 92%, rgba(210, 55, 255, .12), transparent 25%),
                #070d1d !important;
            color: #edf4ff !important;
        }
        [data-testid="stHeader"] { background: rgba(7, 13, 29, .92) !important; }
        .stMainBlockContainer { color: #edf4ff; }
        .stMainBlockContainer label,
        .stMainBlockContainer p,
        .stMainBlockContainer h1,
        .stMainBlockContainer h2,
        .stMainBlockContainer h3,
        .stMainBlockContainer strong { color: #edf4ff !important; }
        .stMainBlockContainer small,
        .stMainBlockContainer [data-testid="stCaptionContainer"] p {
            color: #9aa9c5 !important;
        }

        /* Inputs and compact cards follow the supplied studio reference. */
        .stMainBlockContainer [data-baseweb="select"] > div,
        .stMainBlockContainer input,
        .stMainBlockContainer textarea {
            background: #111a30 !important;
            color: #edf4ff !important;
            border-color: #293652 !important;
        }
        .stMainBlockContainer [data-baseweb="select"] * { color: #edf4ff !important; }
        .stMainBlockContainer [data-testid="stExpander"] details,
        .stMainBlockContainer [data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(15, 24, 45, .82);
            border-color: #293652 !important;
            border-radius: 12px !important;
        }
        .stMainBlockContainer button[kind="primary"] {
            color: #07101f !important;
            border: 0 !important;
            background: linear-gradient(100deg, #35e2dd, #8f7cff 52%, #ff5fa9) !important;
            box-shadow: 0 0 22px rgba(112, 113, 255, .25);
        }
        .stMainBlockContainer button[kind="secondary"] {
            color: #e7efff !important;
            background: #111a30 !important;
            border-color: #33415f !important;
        }
        .stMainBlockContainer [data-baseweb="tab-highlight"] {
            background: linear-gradient(90deg, #38e1dd, #9d75ff, #ff62ae) !important;
        }

        .vm-workflow-strip {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 18px;
            margin: 0.25rem 0 0.55rem;
            padding: 0.55rem 0.8rem;
            border: 1px solid #263551;
            border-radius: 12px;
            background: rgba(13, 22, 42, .92);
        }
        .vm-workflow-title { font-weight: 700; color: #f4f7ff; white-space: nowrap; }
        .vm-workflow-steps { display: flex; align-items: center; justify-content: flex-end; flex: 1; }
        .vm-workflow-step { display: inline-flex; align-items: center; gap: 6px; color: #8998b5; white-space: nowrap; }
        .vm-workflow-step b {
            display: inline-grid;
            place-items: center;
            width: 23px;
            height: 23px;
            border-radius: 50%;
            color: #b8c5dc !important;
            background: #1b2740;
            border: 1px solid #354462;
        }
        .vm-workflow-step.is-active { color: #61e7e2; }
        .vm-workflow-step.is-active b {
            color: #06101d !important;
            border: 0;
            background: linear-gradient(135deg, #37e3dd, #a275ff);
        }
        .vm-workflow-line { width: clamp(20px, 5vw, 70px); height: 1px; margin: 0 9px; background: #34405a; }

        /* The standard pipeline's three primary tabs behave like a creator
           stepper and use the available width instead of tiny text tabs. */
        .stMainBlockContainer [role="tablist"]:has([role="tab"]:nth-child(3)) {
            width: 100%;
        }
        .stMainBlockContainer [role="tablist"]:has([role="tab"]:nth-child(3)) > [role="tab"] {
            flex: 1 1 0;
            justify-content: center;
            border: 1px solid #293752;
            border-radius: 9px 9px 0 0;
        }

        /* Remove Streamlit's presentation-style whitespace. */
        .stMainBlockContainer {
            max-width: 100% !important;
            padding: 0.35rem 1.35rem 0.5rem !important;
        }
        header[data-testid="stHeader"] { height: 2.2rem; }
        [data-testid="stToolbar"] { top: 0.15rem; }

        /* Compact header, tabs, expanders and form spacing. */
        .stMainBlockContainer h3 {
            margin: 0.15rem 0 !important;
            color: #edf4ff !important;
        }
        .stMainBlockContainer [data-testid="stHorizontalBlock"] { gap: 0.65rem; }
        .stMainBlockContainer [data-testid="stVerticalBlock"] { gap: 0.45rem; }
        .stMainBlockContainer [data-baseweb="tab-list"] { gap: 0.2rem; }
        .stMainBlockContainer [data-baseweb="tab"] {
            min-height: 2.35rem;
            padding: 0.35rem 0.65rem;
            white-space: nowrap;
        }
        .stMainBlockContainer [data-testid="stExpander"] details summary {
            min-height: 2.35rem;
            padding: 0.35rem 0.65rem;
        }
        .stMainBlockContainer [data-testid="stAlert"] {
            padding: 0.45rem 0.7rem;
        }
        .stMainBlockContainer p { margin-bottom: 0.15rem; }
        .stMainBlockContainer hr { margin: 0.35rem 0; }

        /* Each creation stage scrolls independently inside one page. */
        .st-key-vm_content_panel,
        .st-key-vm_design_panel,
        .st-key-vm_generate_panel {
            height: var(--vm-panel-height);
            max-height: var(--vm-panel-height);
            min-height: 430px;
            flex: 0 0 var(--vm-panel-height);
            overflow-y: auto;
            overflow-x: hidden;
            border: 1px solid rgba(120, 120, 120, 0.28);
            border-radius: 0.8rem;
            padding: 0.7rem 0.8rem 1rem;
            scrollbar-width: thin;
            background: color-mix(in srgb, var(--background-color) 96%, #7c3aed 4%);
            background: rgba(11, 19, 37, .94);
            border-color: #283753;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.025), 0 14px 35px rgba(0,0,0,.2);
        }
        .st-key-vm_content_panel::-webkit-scrollbar,
        .st-key-vm_design_panel::-webkit-scrollbar,
        .st-key-vm_generate_panel::-webkit-scrollbar { width: 7px; }
        .st-key-vm_content_panel::-webkit-scrollbar-thumb,
        .st-key-vm_design_panel::-webkit-scrollbar-thumb,
        .st-key-vm_generate_panel::-webkit-scrollbar-thumb {
            background: rgba(120,120,120,.4);
            border-radius: 8px;
        }

        /* A stacked, ordinary page is safer on narrow screens. */
        @media (max-width: 900px) {
            :root { --vm-panel-height: auto; }
            .stMainBlockContainer { padding-inline: 0.65rem !important; }
            .st-key-vm_content_panel,
            .st-key-vm_design_panel,
            .st-key-vm_generate_panel {
                height: auto;
                max-height: none;
                min-height: 0;
                flex: initial;
                overflow: visible;
            }
            .vm-workflow-strip { align-items: flex-start; flex-direction: column; }
            .vm-workflow-steps { width: 100%; justify-content: flex-start; overflow-x: auto; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
