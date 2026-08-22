"""Tamil-first content modes used by script and visual prompt generation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ContentMode:
    id: str
    label_ta: str
    label_en: str
    script_structure: str
    visual_preset: str
    voice_profile: str


CONTENT_MODES = (
    ContentMode("story", "தமிழ் கதை", "Tamil story", "hook, setting, conflict, turning point, satisfying ending", "cinematic Tamil storytelling, emotionally coherent scenes", "story"),
    ContentMode("children_story", "குழந்தைகள் கதை", "Children's story", "gentle hook, simple characters, safe challenge, warm lesson", "colourful child-friendly illustration, warm expressions, safe imagery", "children"),
    ContentMode("poetry", "தமிழ் கவிதை", "Tamil poetry", "imagery-led short verses, emotional progression, memorable closing image", "poetic symbolism, soft cinematic light, elegant composition", "poetry"),
    ContentMode("haiku", "தமிழ் ஹைக்கூ", "Tamil haiku", "three concise image-led moments with silence and nature", "minimal nature composition, contemplative atmosphere", "calm"),
    ContentMode("culture", "தமிழ் பண்பாடு", "Tamil culture", "inviting introduction, specific tradition, meaning, present-day relevance", "authentic Tamil material culture, respectful documentary detail", "story"),
    ContentMode("history", "தமிழ் வரலாறு", "Tamil history", "time and place, verified event, people, consequence, legacy", "historically respectful documentary reconstruction, period-appropriate details", "news"),
    ContentMode("education", "தமிழ் கல்வி", "Tamil education", "question, simple explanation, concrete example, recap", "clear educational visual metaphor, uncluttered composition", "natural"),
    ContentMode("news", "செய்திச் சுருக்கம்", "News summary", "headline, verified key facts, context, neutral closing", "clean contemporary news documentary imagery", "news"),
    ContentMode("shorts", "YouTube Shorts", "YouTube Shorts", "immediate hook, rapid value points, strong closing call to action", "bold vertical composition, clear central subject, fast visual rhythm", "motivational"),
    ContentMode("reels", "Instagram Reels", "Instagram Reels", "visual hook, compact story beats, shareable closing", "stylish vertical social composition, vibrant but natural colour", "motivational"),
    ContentMode("product", "தயாரிப்பு விளம்பரம்", "Product promotion", "customer need, product benefit, proof, concise call to action", "premium commercial product photography, clean branded space without text", "motivational"),
    ContentMode("motivation", "ஊக்கமளிக்கும் காணொளி", "Motivational video", "relatable struggle, insight, practical action, uplifting close", "cinematic aspirational imagery, human warmth, forward motion", "motivational"),
)

CONTENT_MODE_MAP = {mode.id: mode for mode in CONTENT_MODES}


def get_content_mode(mode_id: str | None) -> ContentMode:
    return CONTENT_MODE_MAP.get(mode_id or "", CONTENT_MODE_MAP["story"])


def get_content_mode_instruction(mode_id: str | None) -> str:
    mode = get_content_mode(mode_id)
    return (
        f"Selected content mode: {mode.label_en}. "
        f"Structure the complete short video as: {mode.script_structure}. "
        "Do not print these structure labels in the narration."
    )
