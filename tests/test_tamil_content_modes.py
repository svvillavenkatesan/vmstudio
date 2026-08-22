import unittest

from pixelle_video.content_modes import CONTENT_MODES, get_content_mode_instruction
from pixelle_video.prompts.topic_narration import build_topic_narration_prompt
from pixelle_video.utils.prompt_helper import build_image_prompt, build_topic_visual_prefix
from pixelle_video.tts_voices import get_voice_profile


class TamilContentModeTests(unittest.TestCase):
    def test_required_creator_modes_are_available(self):
        mode_ids = {mode.id for mode in CONTENT_MODES}
        self.assertTrue({"story", "children_story", "poetry", "haiku", "culture", "history", "education", "news", "shorts", "reels", "product", "motivation"}.issubset(mode_ids))

    def test_mode_changes_script_structure_instruction(self):
        prompt = build_topic_narration_prompt(
            "தமிழர் பாரம்பரியத்தில் பொங்கல்",
            5,
            5,
            20,
            output_language="Tamil",
            content_mode="culture",
        )
        self.assertIn("Selected content mode: Tamil culture", prompt)
        self.assertIn("specific tradition", prompt)
        self.assertIn("Every narration must be written in Tamil", prompt)

    def test_pongal_topic_context_is_kept_for_every_scene(self):
        prefix = build_topic_visual_prefix(
            "தமிழர் பாரம்பரியத்தில் பொங்கல்",
            content_mode="culture",
            cultural_style="auto",
        )
        scene_prompt = build_image_prompt("A family gathering at sunrise", prefix)
        self.assertIn("kolam at the house entrance", scene_prompt)
        self.assertIn("clay pot boiling over", scene_prompt)
        self.assertIn("sugarcane", scene_prompt)
        self.assertIn("no text, no letters", scene_prompt)

    def test_explicit_cultural_style_overrides_detected_setting(self):
        prefix = build_topic_visual_prefix(
            "தமிழ் நகர வாழ்க்கை",
            content_mode="story",
            cultural_style="modern_chennai",
        )
        self.assertIn("modern Chennai city setting", prefix)

    def test_unknown_mode_falls_back_safely(self):
        self.assertIn("Tamil story", get_content_mode_instruction("not-a-mode"))

    def test_content_modes_recommend_matching_voice_profiles(self):
        from pixelle_video.content_modes import get_content_mode

        self.assertEqual(get_content_mode("children_story").voice_profile, "children")
        self.assertEqual(get_content_mode("haiku").voice_profile, "calm")
        self.assertEqual(get_content_mode("motivation").voice_profile, "motivational")

    def test_voice_profile_has_safe_fallback(self):
        self.assertEqual(get_voice_profile("children")["speed"], 0.9)
        self.assertEqual(get_voice_profile("unknown")["id"], "natural")


if __name__ == "__main__":
    unittest.main()
