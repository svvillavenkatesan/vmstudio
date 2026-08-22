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

"""
International language support for Pixelle-Video Web UI
"""

import json
import locale
from pathlib import Path
from typing import Dict, Optional

from loguru import logger

_locales: Dict[str, dict] = {}
_current_language: str = "en_US"  # Default fallback to English

# Tamil-first product vocabulary.  The locale JSON remains the source for all
# other keys, while these high-traffic labels ensure that the core studio is
# usable in Tamil even while longer help copy is being translated.
_TAMIL_FIRST_OVERRIDES = {
    "app.title": "🎬 VMStudio",
    "content_mode.label": "உள்ளடக்க வகை",
    "content_mode.help": "ஸ்கிரிப்ட் அமைப்பு, காட்சி பாணி மற்றும் குரல் வேகத்திற்கான தயாரான முறை.",
    "cultural_style.label": "கலாச்சாரப் பாணி",
    "cultural_style.help": "தவறான கலாச்சார ஊகங்களைத் தவிர்க்க காட்சியின் தமிழ் சூழலைத் தேர்வு செய்யுங்கள்.",
    "cultural_style.auto": "தலைப்பிலிருந்து தானாக",
    "cultural_style.general_tamil": "பொதுவான தமிழ்நாடு",
    "cultural_style.rural_tamil": "கிராமிய தமிழ்நாடு",
    "cultural_style.modern_chennai": "நவீன சென்னை",
    "cultural_style.chettinad": "செட்டிநாடு",
    "cultural_style.chola": "சோழர் காலம்",
    "cultural_style.sangam": "சங்ககாலம்",
    "cultural_style.temple_arts": "கோவில் மற்றும் கலை",
    "app.subtitle": "தமிழில் உருவாகும் AI வீடியோ ஸ்டுடியோ",
    "language.select": "🌐 மொழி",
    "section.content_input": "📝 கதை / ஸ்கிரிப்ட்",
    "section.bgm": "🎵 பின்னணி இசை",
    "section.tts": "🎤 குரல்",
    "section.image": "🎨 பட உருவாக்கம்",
    "section.video": "🎬 வீடியோ உருவாக்கம்",
    "section.media": "🎨 மீடியா உருவாக்கம்",
    "section.template": "📐 வீடியோ வடிவமைப்பு",
    "section.video_generation": "🎬 இறுதி வீடியோ",
    "subtitle.title": "💬 தமிழ் துணைத்தலைப்புகள்",
    "subtitle.enabled": "துணைத்தலைப்புகளைக் காட்டு",
    "subtitle.mode": "காட்சி முறை",
    "subtitle.mode.standard": "வழக்கமான துணைத்தலைப்பு",
    "subtitle.mode.karaoke": "வார்த்தை-வார்த்தை உத்திரவாதம்",
    "subtitle.mode.bilingual": "தமிழ் / English இருமொழி",
    "subtitle.font": "எழுத்துரு",
    "font.video_text": "வீடியோ தலைப்பு எழுத்துரு",
    "font.video_text_help": "Bundled Noto font பயன்படுத்தப்படுவதால் எல்லா Windows கணினிகளிலும் ஒரே மாதிரியாக வெளிவரும்.",
    "subtitle.size": "எழுத்து அளவு",
    "subtitle.color": "எழுத்து நிறம்",
    "subtitle.highlight_color": "உத்திரவாத நிறம்",
    "subtitle.position": "இடம்",
    "subtitle.position.bottom": "கீழ்",
    "subtitle.position.middle": "நடுவில்",
    "subtitle.position.top": "மேல்",
    "subtitle.safe_zone": "Shorts / Reels பாதுகாப்பான பகுதி",
    "subtitle.composition_help": "துணைத்தலைப்பு AI படத்தில் சேர்க்கப்படாது; இறுதி video composition-ல் மட்டும் பதிக்கப்படும்.",
    "input_mode.topic": "💡 தலைப்பு",
    "input_mode.custom": "✍️ என் ஸ்கிரிப்ட்",
    "input.topic": "தலைப்பு",
    "input.topic_placeholder": "உதாரணம்: தமிழர் பாரம்பரியத்தில் பொங்கல்",
    "input.content": "ஸ்கிரிப்ட்",
    "input.title": "தலைப்பு (விருப்பம்)",
    "input.mode_selector": "உருவாக்கும் முறை",
    "input.output_language": "வீடியோ மொழி",
    "input.output_language.ta": "தமிழ்",
    "input.output_language.en": "English",
    "input.output_language_help": "AI உருவாக்கும் title மற்றும் narration-ன் மொழி. நீங்கள் எழுதும் தலைப்பு எந்த மொழியில் இருந்தாலும் இதைத் தேர்ந்தெடுக்கலாம்.",
    "voice.title": "🎤 குரல் தேர்வு",
    "btn.generate": "🎬 வீடியோ உருவாக்கு",
    "btn.download_video": "⬇️ வீடியோவைப் பதிவிறக்கு",
    "btn.save_config": "💾 அமைப்பை சேமி",
    "btn.test_connection": "இணைப்பைச் சோதிக்கவும்",
    "settings.title": "⚙️ அமைப்புகள்",
    "settings.llm.title": "🤖 மொழி AI அமைப்பு",
    "settings.comfyui.title": "🔧 ComfyUI அமைப்பு",
    "settings.comfyui.local_title": "உள்ளக ComfyUI",
    "settings.comfyui.comfyui_url": "ComfyUI சேவையக முகவரி",
    "tts.inference_mode": "குரல் உருவாக்கும் முறை",
    "tts.mode.local": "உள்ளக குரல்",
    "tts.mode.comfyui": "ComfyUI குரல்",
    "tts.voice_selector": "தமிழ் குரல் தேர்வு",
    "tts.speed": "குரல் வேகம்",
    "tts.preview_title": "குரல் முன்னோட்டம்",
    "tts.preview_text": "முன்னோட்ட உரை",
    "tts.preview_button": "🔊 குரலைக் கேளுங்கள்",
    "tts.voice.ta_IN_PallaviNeural": "தமிழ் பெண் குரல் · இயல்பான (Pallavi)",
    "tts.voice.ta_IN_ValluvarNeural": "தமிழ் ஆண் குரல் · இயல்பான (Valluvar)",
    "tts.profile_selector": "பேசும் பாணி",
    "tts.profile.natural": "இயல்பான குரல்",
    "tts.profile.news": "செய்தி வாசிப்பு",
    "tts.profile.story": "கதை சொல்லல்",
    "tts.profile.poetry": "கவிதை வாசிப்பு",
    "tts.profile.children": "குழந்தைகள் கதை — மென்மை",
    "tts.profile.calm": "அமைதியான வாசிப்பு",
    "tts.profile.motivational": "ஊக்கமளிக்கும் வாசிப்பு",
    "tts.profile_hint": "Local Tamil voice-ல் இவை வேக (tempo) presets மட்டுமே. உணர்ச்சி மிக்க அல்லது clone செய்யப்பட்ட குரலுக்கு ComfyUI TTS workflow பயன்படுத்தவும்.",
    "style.workflow": "உருவாக்கும் workflow",
    "style.prompt_prefix": "காட்சி பாணி வழிகாட்டி",
    "style.prompt_prefix_help": "தலைப்பு தமிழ்ப் பண்பாட்டைச் சார்ந்தால் பொருத்தமான காட்சி விவரங்கள் தானாக சேர்க்கப்படும். படத்தில் தமிழ் எழுத்தை உருவாக்க வேண்டாம்; அது இறுதி video overlay-ல் சேர்க்கப்படும்.",
    "art_style.label": "காட்சி கலைப் பாணி",
    "art_style.help": "இவை இலவச prompt presets. கிடைக்கும் தோற்றமும் தரமும் தேர்ந்தெடுத்த ComfyUI model-ஐச் சார்ந்தது.",
    "art_style.applied": "பயன்படுத்தப்படும் பாணி: {style}",
    "duration.one_minute": "⏱️ 1 நிமிடம் · 4 காட்சிகள்",
    "duration.one_minute_help": "நான்கு விரிவான narration காட்சிகளுடன் சுமார் ஒரு நிமிட வீடியோ உருவாக்கும் preset.",
    "animation.label": "பட இயக்கம்",
    "animation.cinematic": "🎥 Cinematic zoom / pan",
    "animation.none": "நிலையான படம்",
    "animation.help": "ஒவ்வொரு AI படத்திற்கும் narration நேரத்திற்கு ஏற்ப தனித்த camera movement சேர்க்கப்படும்.",
    "template.selector": "Video template தேர்வு",
    "template.type.static": "📄 உரை மைய வடிவம்",
    "template.type.image": "🖼️ படங்களுடன்",
    "template.type.video": "🎬 வீடியோ காட்சிகளுடன்",
    "template.select_button": "தேர்வு செய்",
    "template.selected": "தேர்ந்தெடுக்கப்பட்டது",
    "template.selected_template": "தற்போதைய வடிவமைப்பு",
    "history.page_title": "📚 உருவாக்க வரலாறு",
    "history.no_tasks": "இன்னும் எந்த வீடியோவும் உருவாக்கப்படவில்லை",
    "status.generating": "🚀 வீடியோ உருவாகிறது...",
    "status.success": "✅ வீடியோ வெற்றிகரமாக உருவாக்கப்பட்டது!",
    "status.error": "❌ உருவாக்கம் தோல்வியடைந்தது: {error}",
    "error.input_required": "❌ தலைப்பு அல்லது ஸ்கிரிப்டை உள்ளிடுங்கள்",
    "error.video_workflow_required": "வீடியோவை உருவாக்கும் முன், ஒரு video workflow அல்லது API video model-ஐத் தேர்ந்தெடுங்கள்.",
    "history.action.delete_confirm": "⚠️ இந்த வீடியோ பதிவை நீக்க வேண்டுமா? இதை மீட்டெடுக்க முடியாது.",
    "history.action.delete_failed": "❌ பதிவை நீக்க முடியவில்லை: {error}",
    "history.detail.not_found": "கோரப்பட்ட வீடியோ பதிவு கிடைக்கவில்லை.",
    "help.feature_description": "💡 இந்த வசதியைப் பற்றி",
    "help.what": "எதற்காக",
    "help.how": "எப்படி பயன்படுத்துவது",
    "pipeline.quick_create.name": "விரைவாக உருவாக்கு",
    "pipeline.quick_create.description": "தலைப்பு அல்லது உங்கள் ஸ்கிரிப்ட்டிலிருந்து வீடியோ உருவாக்குங்கள்.",
    "input.text": "உரை",
    "input.text_help_generate": "AI ஸ்கிரிப்ட் உருவாக்க ஒரு தலைப்பை உள்ளிடுங்கள்.",
    "input.text_help_fixed": "உங்கள் முழு குரலுரையை உள்ளிடுங்கள்.",
    "input.content_placeholder": "ஒவ்வொரு காட்சிக்கான உரையைப் பத்தி அல்லது வரியாக உள்ளிடுங்கள்.",
    "input.title_placeholder": "காலியாக விட்டால் தானாக உருவாக்கப்படும்.",
    "input.title_help": "வீடியோவிற்கான விருப்பத் தலைப்பு.",
    "split.mode_label": "உரையைப் பிரிக்கும் முறை",
    "split.mode_help": "உரை எவ்வாறு காட்சிகளாகப் பிரிக்கப்பட வேண்டும் என்பதைத் தேர்ந்தெடுங்கள்.",
    "split.mode_paragraph": "📄 பத்தியாக",
    "split.mode_line": "📝 வரியாக",
    "split.mode_sentence": "✂️ வாக்கியமாக",
    "video.frames": "காட்சிகள்",
    "video.frames_label": "{n} காட்சிகள்",
    "video.frames_help": "AI உருவாக்க வேண்டிய காட்சிகளின் எண்ணிக்கை.",
    "video.frames_fixed_mode_hint": "உங்கள் உரையின் பிரிவுகளே காட்சிகளாகும்.",
    "bgm.none": "🔇 பின்னணி இசை இல்லை",
    "bgm.volume": "ஒலி அளவு",
    "bgm.volume_help": "பின்னணி இசையின் ஒலி அளவை மாற்றுங்கள்.",
    "bgm.preview": "▶ இசையைக் கேளுங்கள்",
    "bgm.preview_failed": "❌ இசைக் கோப்பு கிடைக்கவில்லை: {file}",
    "tts.what": "உரையை இயல்பான பேச்சாக மாற்றும்.",
    "tts.mode.local_hint": "கணினியில் நேரடியாக Edge TTS பயன்படுத்தப்படும்.",
    "tts.mode.comfyui_hint": "உணர்ச்சி அல்லது voice cloning workflow-ஐப் பயன்படுத்தும்.",
    "tts.speed_label": "குரல் வேகம்: {speed}x",
    "tts.previewing": "குரல் முன்னோட்டம் உருவாகிறது...",
    "tts.preview_success": "✅ குரல் முன்னோட்டம் தயார்.",
    "tts.preview_failed": "குரல் முன்னோட்டம் தோல்வி: {error}",
    "template.gallery_view": "வடிவமைப்புகள்",
    "template.preview_title": "வடிவமைப்பு முன்னோட்டம்",
    "template.preview_button": "🖼️ முன்னோட்டம் உருவாக்கு",
    "template.preview_generating": "முன்னோட்டம் உருவாகிறது...",
    "template.preview_success": "✅ முன்னோட்டம் தயார்.",
    "template.preview_failed": "❌ முன்னோட்டம் தோல்வி: {error}",
    "template.video_size_info": "இறுதி வீடியோ அளவு: {width} × {height}",
    "image.not_required": "தேர்ந்தெடுத்த வடிவமைப்பிற்கு AI படம் தேவையில்லை.",
    "image.not_required_hint": "உரை மட்டுமே கொண்ட வடிவமைப்பு; விரைவாகவும் குறைந்த செலவிலும் உருவாகும்.",
    "settings.not_configured": "⚠️ AI சேவை அமைப்பு முழுமையாக உள்ளிடப்படவில்லை.",
    "progress.generating_title": "தலைப்பு உருவாகிறது...",
    "progress.generating_narrations": "குரலுரை உருவாகிறது...",
    "progress.splitting_script": "ஸ்கிரிப்ட் பிரிக்கப்படுகிறது...",
    "progress.generating_image_prompts": "காட்சி விவரங்கள் உருவாகின்றன...",
    "progress.step_audio": "குரல் உருவாக்கம்",
    "progress.step_image": "பட உருவாக்கம்",
    "progress.concatenating": "காட்சிகள் இணைக்கப்படுகின்றன...",
    "progress.completed": "✅ முடிவடைந்தது",
    "history.filter_status": "நிலை வடிகட்டி",
    "history.status_all": "அனைத்தும்",
    "history.status_completed": "முடிவடைந்தவை",
    "history.status_running": "உருவாகிக் கொண்டிருப்பவை",
    "history.status_failed": "தோல்வியடைந்தவை",
    "history.task_card.view_detail": "விவரங்களைப் பார்",
    "history.task_card.download": "வீடியோவைப் பதிவிறக்கு",
    "history.task_card.delete": "பதிவை நீக்கு",
    "history.detail.close": "மூடு",
    "history.action.delete_success": "✅ பதிவு நீக்கப்பட்டது.",
    "batch.mode_label": "🔢 பல வீடியோக்கள்",
    "batch.mode_help": "ஒரு வரிக்கு ஒரு தலைப்பாகப் பல வீடியோக்களை உருவாக்கும்.",
    "batch.topics_label": "தலைப்புகள்",
    "batch.generate_button": "🎬 அனைத்து வீடியோக்களையும் உருவாக்கு",
    "draft.title": "📁 என் திட்டங்கள்",
    "draft.empty": "சேமிக்கப்பட்ட draft இன்னும் இல்லை. தலைப்பை எழுதத் தொடங்கினால் தானாகச் சேமிக்கப்படும்.",
    "draft.choose": "திட்டத்தைத் தேர்வு செய்யுங்கள்",
    "draft.open": "📂 மீண்டும் திற",
    "draft.new": "➕ புதிய வீடியோ",
    "draft.delete": "🗑️ நீக்கு",
    "draft.delete_confirm": "நீக்குவதை உறுதிப்படுத்து",
    "draft.untitled": "பெயரிடாத திட்டம்",
}


def load_locales() -> Dict[str, dict]:
    """Load all locale files from locales directory"""
    global _locales
    
    locales_dir = Path(__file__).parent / "locales"
    
    if not locales_dir.exists():
        logger.warning(f"Locales directory not found: {locales_dir}")
        return _locales
    
    for json_file in locales_dir.glob("*.json"):
        lang_code = json_file.stem
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                _locales[lang_code] = json.load(f)
            logger.debug(f"Loaded locale: {lang_code}")
        except Exception as e:
            logger.error(f"Failed to load locale {lang_code}: {e}")
    
    logger.info(f"Loaded {len(_locales)} locales: {list(_locales.keys())}")
    return _locales


def set_language(lang_code: str):
    """Set current language"""
    global _current_language
    if lang_code in _locales:
        _current_language = lang_code
        logger.debug(f"Language set to: {lang_code}")
    else:
        logger.warning(f"Language {lang_code} not found, keeping {_current_language}")


def get_language() -> str:
    """Get current language"""
    return _current_language


def tr(key: str, fallback: Optional[str] = None, **kwargs) -> str:
    """
    Translate a key to current language
    
    Args:
        key: Translation key (e.g., "app.title")
        fallback: Fallback text if key not found
        **kwargs: Format parameters for string interpolation
    
    Returns:
        Translated text
    
    Example:
        tr("app.title")  # => "Pixelle-Video"
        tr("error.missing_field", field="API Key")  # => "请填写 API Key"
    """
    locale = _locales.get(_current_language, {})
    translations = locale.get("t", {})
    result = (
        _TAMIL_FIRST_OVERRIDES.get(key)
        if _current_language == "ta_IN"
        else translations.get(key)
    )
    if result is None:
        result = translations.get(key)
    
    if result is None:
        # Try fallback parameter
        if fallback is not None:
            result = fallback
        # Try English fallback
        elif _current_language != "en_US" and "en_US" in _locales:
            en_locale = _locales["en_US"]
            result = en_locale.get("t", {}).get(key)
        
        # Last resort: return the key itself
        if result is None:
            result = key
            logger.debug(f"Translation missing: {key}")
    
    # Apply string interpolation if kwargs provided
    if kwargs:
        try:
            result = result.format(**kwargs)
        except (KeyError, ValueError) as e:
            logger.warning(f"Failed to format translation '{key}': {e}")
    
    return result


def get_language_name(lang_code: Optional[str] = None) -> str:
    """Get display name of a language"""
    if lang_code is None:
        lang_code = _current_language
    
    locale = _locales.get(lang_code, {})
    return locale.get("language_name", lang_code)


def get_available_languages() -> Dict[str, str]:
    """Get all available languages with their display names"""
    return {
        code: locale.get("language_name", code)
        for code, locale in _locales.items()
    }


def detect_system_language() -> str:
    """
    Detect system/OS language and return the best matching locale code.
    Falls back to English if no match found.
    
    This is designed for self-hosted scenarios where the server and browser
    are typically on the same machine.
    
    Returns:
        Language code (e.g., "zh_CN", "en_US")
    """
    try:
        import os
        import platform
        import subprocess
        
        system_locale = None
        
        # Method 1: macOS-specific detection (most reliable for macOS)
        if platform.system() == "Darwin":  # macOS
            try:
                # Get AppleLocale which reflects system language preference
                result = subprocess.run(
                    ["defaults", "read", "-g", "AppleLocale"],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                if result.returncode == 0:
                    system_locale = result.stdout.strip()
                    logger.debug(f"System locale from macOS AppleLocale: {system_locale}")
            except Exception as e:
                logger.debug(f"macOS AppleLocale detection failed: {e}")
            
            # Fallback: try AppleLanguages
            if not system_locale:
                try:
                    result = subprocess.run(
                        ["defaults", "read", "-g", "AppleLanguages"],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    if result.returncode == 0:
                        # Parse array output like: ( "zh-Hans-CN", "en-CN" )
                        output = result.stdout.strip()
                        # Extract first language
                        import re
                        match = re.search(r'"([^"]+)"', output)
                        if match:
                            lang = match.group(1)
                            # Convert zh-Hans-CN to zh_CN
                            if lang.startswith("zh-Hans"):
                                system_locale = "zh_CN"
                            elif lang.startswith("zh-Hant"):
                                system_locale = "zh_TW"
                            else:
                                system_locale = lang.replace("-", "_")
                            logger.debug(f"System locale from macOS AppleLanguages: {system_locale}")
                except Exception as e:
                    logger.debug(f"macOS AppleLanguages detection failed: {e}")
        
        # Method 2: Get from environment locale (cross-platform)
        if not system_locale:
            try:
                system_locale = locale.getdefaultlocale()[0]
                logger.debug(f"System locale from getdefaultlocale(): {system_locale}")
            except Exception as e:
                logger.debug(f"getdefaultlocale() failed: {e}")
        
        # Method 3: Get from current locale
        if not system_locale:
            try:
                system_locale = locale.getlocale()[0]
                logger.debug(f"System locale from getlocale(): {system_locale}")
            except Exception as e:
                logger.debug(f"getlocale() failed: {e}")
        
        # Method 4: Try to get from environment variables
        if not system_locale:
            for env_var in ['LC_ALL', 'LC_MESSAGES', 'LANG', 'LANGUAGE']:
                env_value = os.environ.get(env_var)
                if env_value:
                    # Extract language code from formats like "zh_CN.UTF-8"
                    system_locale = env_value.split('.')[0]
                    logger.debug(f"System locale from {env_var}: {system_locale}")
                    break
        
        if system_locale:
            # Normalize the locale string
            # Handle formats: zh_CN, zh-CN, zh_CN.UTF-8, etc.
            system_locale = system_locale.replace('-', '_').split('.')[0]
            
            # Direct match (e.g., "zh_CN")
            for locale_code in _locales.keys():
                if locale_code.lower() == system_locale.lower():
                    logger.info(f"System language matched: {locale_code}")
                    return locale_code
            
            # Partial match (e.g., "zh" matches "zh_CN")
            lang_prefix = system_locale.split('_')[0].lower()
            for locale_code in _locales.keys():
                if locale_code.lower().startswith(lang_prefix):
                    logger.info(f"System language partially matched: {locale_code} (from {system_locale})")
                    return locale_code
        
        logger.info("No system language detected, using fallback")
    except Exception as e:
        logger.warning(f"Failed to detect system language: {e}")
    
    # Fallback to English
    return "en_US"


# Auto-load locales on import
load_locales()

# Auto-detect and set system language
_detected_language = detect_system_language()
_current_language = _detected_language
logger.info(f"Default language initialized to: {_current_language}")

