"""Model-independent visual art style prompt presets."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ArtStyle:
    id: str
    label_en: str
    label_ta: str
    prompt: str


ART_STYLES = (
    ArtStyle("auto", "Automatic / No preset", "தானியங்கி / தனிப் பாணி இல்லை", ""),
    ArtStyle("cinematic_art", "Cinematic Art", "சினிமாட்டிக் கலை", "cinematic concept artwork, dramatic lighting, filmic colour grading, strong visual storytelling"),
    ArtStyle("concept_art", "Concept Art", "கருத்துருவக் கலை", "professional concept art, exploratory world design, atmospheric lighting, detailed visual development"),
    ArtStyle("fantasy_art", "Fantasy Art", "கற்பனைக் கலை", "epic fantasy art, imaginative world, magical atmosphere, ornate environmental detail"),
    ArtStyle("dark_fantasy", "Dark Fantasy", "இருண்ட கற்பனைக் கலை", "dark fantasy art, mysterious atmosphere, dramatic shadows, gothic detail, non-graphic imagery"),
    ArtStyle("anime_manga", "Anime / Manga", "அனிமே / மாங்கா", "anime and manga-inspired illustration, expressive characters, clean linework, dynamic composition"),
    ArtStyle("comic_book", "Comic Book Art", "காமிக் புத்தகக் கலை", "comic book illustration, bold ink lines, dynamic framing, halftone texture, vivid colour blocks"),
    ArtStyle("3d_render", "3D Render", "3D வடிவமைப்பு", "high-quality 3D render, realistic materials, global illumination, detailed modelling"),
    ArtStyle("3d_cartoon", "3D Cartoon", "3D கார்ட்டூன்", "stylized 3D cartoon, friendly rounded forms, expressive characters, colourful soft lighting"),
    ArtStyle("pixel_art", "Pixel Art", "பிக்சல் கலை", "pixel art, deliberate limited palette, crisp pixel clusters, retro game composition"),
    ArtStyle("low_poly", "Low Poly", "லோ பாலி கலை", "low-poly 3D art, faceted geometry, simplified forms, clean stylized lighting"),
    ArtStyle("matte_painting", "Matte Painting", "மேட் ஓவியம்", "cinematic matte painting, vast environment, realistic atmospheric depth, epic scale"),
    ArtStyle("digital_illustration", "Digital Illustration", "டிஜிட்டல் விளக்கப்படம்", "polished digital illustration, refined shapes, rich colour, detailed painterly finish"),
    ArtStyle("editorial_illustration", "Editorial Illustration", "ஆசிரியர் விளக்கப்படம்", "editorial illustration, intelligent visual metaphor, simplified composition, contemporary print aesthetic"),
    ArtStyle("childrens_book", "Children's Book Illustration", "குழந்தைகள் புத்தக ஓவியம்", "warm children's book illustration, gentle shapes, friendly expressions, colourful safe imagery"),
    ArtStyle("vintage_poster", "Vintage Poster", "பழமையான சுவரொட்டி", "vintage poster illustration, aged print texture, limited colour palette, bold graphic composition without text"),
    ArtStyle("art_nouveau", "Art Nouveau", "ஆர்ட் நுவோ", "Art Nouveau-inspired illustration, flowing organic curves, botanical ornament, elegant decorative framing"),
    ArtStyle("art_deco", "Art Deco", "ஆர்ட் டெகோ", "Art Deco-inspired design, geometric symmetry, luxurious metallic accents, streamlined elegance"),
    ArtStyle("steampunk", "Steampunk", "ஸ்டீம்பங்க்", "steampunk art, brass mechanical details, retro-futurist machinery, warm industrial atmosphere"),
    ArtStyle("cyberpunk", "Cyberpunk", "சைபர்பங்க்", "cyberpunk art, futuristic city, neon reflections, high-tech atmosphere, cinematic contrast"),
    ArtStyle("neon_futuristic", "Neon / Futuristic Art", "நியான் / எதிர்காலக் கலை", "futuristic neon art, luminous accents, sleek technology, vivid atmospheric glow"),
    ArtStyle("paper_cut", "Paper Cut Art", "காகித வெட்டுக் கலை", "layered paper-cut illustration, tactile paper fibres, crafted edges, dimensional shadows"),
    ArtStyle("clay_stop_motion", "Clay / Stop-motion Style", "களிமண் / ஸ்டாப் மோஷன்", "handcrafted clay stop-motion style, tactile modelling, miniature set, soft studio lighting"),
    ArtStyle("woodcut_linocut", "Woodcut / Linocut", "மரச்செதுக்கு / லினோகட்", "woodcut and linocut print style, carved bold lines, high contrast, handmade ink texture"),
    ArtStyle("stained_glass", "Stained Glass", "வண்ணக் கண்ணாடிக் கலை", "stained-glass artwork, luminous coloured panes, dark leading lines, decorative composition"),
    ArtStyle("collage", "Collage", "கொலாஜ்", "artistic collage, layered cut-paper imagery, varied textures, balanced editorial composition"),
    ArtStyle("mixed_media", "Mixed Media", "கலப்பு ஊடகக் கலை", "mixed-media artwork, paint, paper and textured marks, expressive layered composition"),
)

ART_STYLE_MAP = {style.id: style for style in ART_STYLES}


def get_art_style(style_id: str | None) -> ArtStyle:
    return ART_STYLE_MAP.get(style_id or "", ART_STYLE_MAP["auto"])


def apply_art_style(prefix: str, style_id: str | None) -> str:
    style_prompt = get_art_style(style_id).prompt
    return ", ".join(part.strip() for part in (style_prompt, prefix) if part and part.strip())
