import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pixelle_video.prompts.content_narration import build_content_narration_prompt
from pixelle_video.prompts.title_generation import build_title_generation_prompt
from pixelle_video.prompts.topic_narration import build_topic_narration_prompt
from web.i18n import set_language, tr
from pixelle_video.services.frame_html import HTMLFrameGenerator
from pixelle_video.utils.content_generators import generate_subtitle_translations
from web.components.output_preview import requires_llm_configuration


class BilingualGenerationTests(unittest.TestCase):
    def test_fixed_static_video_with_title_does_not_require_llm(self) -> None:
        self.assertFalse(
            requires_llm_configuration(
                {
                    "mode": "fixed",
                    "title": "தமிழ் வீடியோ",
                    "subtitle_settings": {"mode": "standard"},
                }
            )
        )

    def test_bilingual_subtitles_require_llm_translation(self) -> None:
        self.assertTrue(
            requires_llm_configuration(
                {
                    "mode": "fixed",
                    "title": "Tamil video",
                    "subtitle_settings": {"mode": "bilingual"},
                }
            )
        )

    def test_tamil_topic_can_request_english_video(self) -> None:
        prompt = build_topic_narration_prompt(
            "பொங்கல்", 3, 5, 20, output_language="English"
        )
        self.assertIn("Every narration must be written in English", prompt)
        self.assertIn("Strictly use English, even when the topic was entered", prompt)

    def test_english_content_can_request_tamil_video(self) -> None:
        prompt = build_content_narration_prompt(
            "History of Madurai", 3, 5, 20, output_language="Tamil"
        )
        self.assertIn("Write every narration in **Tamil**", prompt)
        self.assertIn("selected output language", prompt)

    def test_title_uses_selected_output_language(self) -> None:
        prompt = build_title_generation_prompt(
            "History of Madurai", output_language="Tamil"
        )
        self.assertIn("MUST be in **Tamil**", prompt)

    def test_core_download_label_is_localized(self) -> None:
        try:
            set_language("ta_IN")
            self.assertIn("பதிவிறக்கு", tr("btn.download_video"))
            set_language("en_US")
            self.assertEqual(tr("btn.download_video"), "⬇️ Download Video")
        finally:
            set_language("ta_IN")

    def test_subtitle_layer_escapes_text_and_uses_safe_zone(self) -> None:
        with TemporaryDirectory() as directory:
            template_dir = Path(directory) / "1080x1920"
            template_dir.mkdir()
            template = template_dir / "template.html"
            template.write_text("<html><body>{{text}}</body></html>", encoding="utf-8")
            generator = HTMLFrameGenerator(str(template))
            rendered = generator._inject_subtitle_layer(
                "<html><body></body></html>",
                "<script>unsafe</script>",
                "Safe translation",
                {
                    "enabled": True,
                    "mode": "bilingual",
                    "position": "bottom",
                    "safe_zone": True,
                },
            )
        self.assertNotIn("<script>unsafe</script>", rendered)
        self.assertIn("&lt;script&gt;unsafe&lt;/script&gt;", rendered)
        self.assertIn("bottom: 260px", rendered)
        self.assertIn("Safe translation", rendered)


class SubtitleTranslationTests(unittest.IsolatedAsyncioTestCase):
    async def test_bilingual_translation_preserves_segment_count(self) -> None:
        async def fake_llm(**_kwargs):
            return '{"translations": ["First", "Second"]}'

        result = await generate_subtitle_translations(
            fake_llm, ["ஒன்று", "இரண்டு"], "English"
        )
        self.assertEqual(result, ["First", "Second"])


if __name__ == "__main__":
    unittest.main()
