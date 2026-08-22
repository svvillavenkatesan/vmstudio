import unittest
from types import SimpleNamespace

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

    def test_pongal_script_prompt_has_factual_guardrails(self):
        prompt = build_topic_narration_prompt(
            "தமிழர் பாரம்பரியத்தில் பொங்கல்", 3, 8, 22, "Tamil", "culture"
        )
        self.assertIn("அறுவடைத் திருவிழா", prompt)
        self.assertIn("அதை மதம் என்று குறிப்பிட வேண்டாம்", prompt)
        self.assertNotIn("Chinese punctuation", prompt)

    def test_compact_local_prompt_preserves_required_json_key(self):
        from pixelle_video.prompts.topic_narration import build_compact_topic_narration_prompt

        prompt = build_compact_topic_narration_prompt(
            "தமிழர் பாரம்பரியத்தில் பொங்கல்", 3, 8, 22, "Tamil", "culture"
        )
        self.assertIn('"narrations"', prompt)
        self.assertIn("ஒரே கருத்தை மீண்டும் சொல்லாதே", prompt)


class OfflineVisualPromptTests(unittest.IsolatedAsyncioTestCase):
    async def test_fixed_script_can_use_supplied_prompts_without_llm(self):
        from pixelle_video.pipelines.standard import StandardPipeline

        pipeline = object.__new__(StandardPipeline)
        pipeline.core = SimpleNamespace(config={"comfyui": {"image": {"prompt_prefix": ""}}})
        context = SimpleNamespace(
            params={
                "frame_template": "1080x1920/image_tamil_festival.html",
                "image_prompts": ["Pongal pot", "sugarcane harvest"],
                "content_mode": "culture",
                "cultural_style": "rural_tamil",
            },
            input_text="பொங்கல்",
            narrations=["ஒன்று", "இரண்டு"],
            progress_callback=None,
            image_prompts=[],
        )
        await pipeline.plan_visuals(context)
        self.assertEqual(len(context.image_prompts), 2)
        self.assertIn("Pongal pot", context.image_prompts[0])
        self.assertIn("no text, no letters", context.image_prompts[0])

    async def test_cleanup_accepts_comfykit_backend_without_close(self):
        from pixelle_video.service import PixelleVideoCore

        core = object.__new__(PixelleVideoCore)
        core._comfykit = object()
        core._comfykit_config_hash = "test"
        await core.cleanup()
        self.assertIsNone(core._comfykit)


class LocalLLMPresetTests(unittest.TestCase):
    def test_ollama_preset_uses_tamil_capable_local_model(self):
        from pixelle_video.llm_presets import get_preset

        preset = get_preset("Ollama")
        self.assertEqual(preset["base_url"], "http://127.0.0.1:11434/v1")
        self.assertEqual(preset["model"], "qwen3:1.7b")
        self.assertEqual(preset["default_api_key"], "ollama")

    def test_qwen3_uses_fast_non_reasoning_mode(self):
        from pixelle_video.services.llm_service import LLMService

        prompt = LLMService._prepare_prompt_for_model("தமிழில் எழுதுக", "qwen3:1.7b")
        self.assertTrue(prompt.startswith("/no_think\n"))
        self.assertEqual(
            LLMService._prepare_prompt_for_model("தமிழில் எழுதுக", "gpt-4o"),
            "தமிழில் எழுதுக",
        )
        self.assertEqual(
            LLMService._prepare_kwargs_for_model({}, "qwen3:1.7b")["reasoning_effort"],
            "none",
        )


if __name__ == "__main__":
    unittest.main()
