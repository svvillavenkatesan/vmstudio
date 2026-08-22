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

"""Prompt helpers for VMStudio.

The image model is deliberately asked for text-free imagery.  Tamil titles,
captions, and subtitles belong in the HTML composition layer where Unicode
fonts render them correctly.
"""

import re


_TAMIL_CULTURAL_SIGNALS = {
    ("பொங்கல்", "thai pongal", "pongal"): (
        "authentic Tamil Pongal celebration, kolam at the house entrance, clay pot "
        "boiling over, sugarcane, turmeric plants, warm rural Tamil Nadu setting"
    ),
    ("தமிழர்", "tamil culture", "tamil heritage", "தமிழ் பண்பாடு"): (
        "authentic Tamil cultural setting, respectful traditional clothing, local "
        "architecture and crafts, natural South Indian light"
    ),
    ("கோவில்", "temple", "கோயில்"): (
        "Tamil temple architecture, stone carvings, respectful devotional atmosphere, "
        "no readable text or signage"
    ),
    ("பாரதியார்", "bharathiyar", "கவிதை", "poem", "poetry"): (
        "evocative Tamil literary visual language, symbolic imagery, textured paper "
        "and ink atmosphere, no letters or typography in the image"
    ),
    ("சங்கம்", "sangam", "சோழ", "chola", "பாண்டிய", "pandya"): (
        "historically respectful ancient Tamil setting, period-appropriate dress, "
        "architecture and objects, cinematic documentary composition"
    ),
}

_TAMIL_SCRIPT_CONTEXT = {
    ("பொங்கல்", "thai pongal", "pongal"): (
        "பொங்கல் தமிழர் அறுவடைத் திருவிழா. தை மாதத்தில் கொண்டாடப்படுகிறது. "
        "புதுப் பானையில் பால் பொங்கச் செய்து நன்றி செலுத்துதல், வாசல் கோலம், "
        "கரும்பு மற்றும் சூரியனுக்கு மரியாதை செலுத்துதல் முக்கிய கூறுகள். "
        "அதை மதம் என்று குறிப்பிட வேண்டாம்."
    ),
    ("சோழ", "chola"): (
        "சோழர் வரலாற்றைப் பேசும்போது காலம், இடம் மற்றும் ஆதாரம் உறுதியான தகவல்களை மட்டும் பயன்படுத்து. "
        "கல்வெட்டுகள், நீர்ப்பாசனம், கடல் வாணிபம், கோவில் கட்டிடக்கலை போன்ற பொருத்தமான கூறுகளைச் சூழலுடன் கூறு."
    ),
    ("திருக்குறள்", "thirukkural"): (
        "திருக்குறள் 133 அதிகாரங்களையும் 1330 குறள்களையும் கொண்டது. "
        "சரிபார்க்காத குறள் எண் அல்லது மூலவரியை உருவாக்க வேண்டாம்; கருத்தை விளக்கும்போது உரைநடையில் தெளிவாகக் கூறு."
    ),
    ("பாரதியார்", "bharathiyar"): (
        "பாரதியாரைப் பற்றிய உள்ளடக்கத்தில் சரிபார்க்காத பாடல் வரிகளை மேற்கோளாக உருவாக்க வேண்டாம். "
        "விடுதலை, சமத்துவம், பெண்முன்னேற்றம் மற்றும் தமிழ்ப்பற்று போன்ற அறியப்பட்ட கருப்பொருள்களைத் தெளிவாகச் சொல்."
    ),
}

_CULTURAL_STYLES = {
    "general_tamil": "authentic contemporary Tamil Nadu setting, locally appropriate clothing, architecture and objects",
    "rural_tamil": "authentic rural Tamil Nadu village, local homes, fields, natural materials and traditional everyday clothing",
    "modern_chennai": "modern Chennai city setting, contemporary Tamil people, locally accurate streets and architecture",
    "chettinad": "authentic Chettinad setting, heritage courtyard architecture, Athangudi tile patterns and regionally appropriate details",
    "chola": "historically respectful Chola-period Tamil setting, period-appropriate architecture, dress and objects, no modern items",
    "sangam": "careful Sangam-era Tamil visual interpretation, period-appropriate landscape, dress and objects, no modern items",
    "temple_arts": "Tamil temple and performing-arts setting, respectful iconography, traditional textiles and instruments",
}


def get_tamil_cultural_context(prompt: str) -> str:
    """Return a visual context only when the topic explicitly calls for one.

    This avoids forcing cultural imagery into unrelated Tamil topics such as
    software tutorials or business news.
    """
    normalized = prompt.casefold()
    for signals, context in _TAMIL_CULTURAL_SIGNALS.items():
        if any(signal.casefold() in normalized for signal in signals):
            return context
    return ""


def get_tamil_script_context(topic: str) -> str:
    """Return concise factual anchors for Tamil narration generation."""
    normalized = topic.casefold()
    for signals, context in _TAMIL_SCRIPT_CONTEXT.items():
        if any(signal.casefold() in normalized for signal in signals):
            return context
    return "குறிப்பிட்ட தகவல் உறுதியாகத் தெரியாவிட்டால் அதை உருவாக்க வேண்டாம்; பொதுவான, துல்லியமான விளக்கத்தை மட்டும் கொடு."


def build_topic_visual_prefix(
    topic: str,
    prefix: str = "",
    content_mode: str = "story",
    cultural_style: str = "auto",
) -> str:
    """Build visual context that remains consistent across every scene."""
    from pixelle_video.content_modes import get_content_mode

    mode = get_content_mode(content_mode)
    detected_context = get_tamil_cultural_context(topic)
    selected_context = "" if cultural_style == "auto" else _CULTURAL_STYLES.get(cultural_style, "")
    parts = [prefix.strip(), mode.visual_preset, selected_context or detected_context]
    return ", ".join(part for part in parts if part)


def build_image_prompt(prompt: str, prefix: str = "") -> str:
    """
    Build final image prompt with optional prefix
    
    Args:
        prompt: User's raw prompt
        prefix: Optional prefix to add before the prompt
    
    Returns:
        Final prompt with prefix applied (if provided)
    
    Examples:
        >>> build_image_prompt("a cat", "")
        'a cat'
        
        >>> build_image_prompt("a cat", "anime style")
        'anime style, a cat'
        
        >>> build_image_prompt("a cat", "  anime style  ")
        'anime style, a cat'
    """
    prefix = prefix.strip() if prefix else ""
    prompt = prompt.strip() if prompt else ""
    
    cultural_context = get_tamil_cultural_context(prompt)
    # Image generators are unreliable at Tamil typography.  Text is added by
    # templates after generation, never baked into the generated background.
    typography_guard = "no text, no letters, no typography, no watermark"
    parts = [part for part in (prefix, cultural_context, prompt, typography_guard) if part]

    if parts:
        return ", ".join(parts)
    return ""

