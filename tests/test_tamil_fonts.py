import unittest

from pixelle_video.services.frame_html import HTMLFrameGenerator
from pixelle_video.utils.font_manager import (
    bundled_font_face_css,
    font_family_css,
    normalize_font_name,
)


class TamilFontPackTests(unittest.TestCase):
    def test_bundled_font_faces_are_self_contained(self):
        css = bundled_font_face_css()
        self.assertIn("font-family: 'Noto Sans Tamil'", css)
        self.assertIn("font-family: 'Noto Serif Tamil'", css)
        self.assertIn("data:font/ttf;base64,", css)

    def test_unknown_font_uses_safe_default(self):
        self.assertEqual(normalize_font_name("Unknown Font"), "Noto Sans Tamil")
        self.assertIn("Noto Sans Tamil", font_family_css("Unknown Font"))

    def test_selected_text_font_is_injected_into_template(self):
        generator = object.__new__(HTMLFrameGenerator)
        rendered = generator._inject_tamil_font_pack(
            "<html><head></head><body></body></html>",
            {"text_font": "Noto Serif Tamil"},
        )
        self.assertIn("NotoSerif", rendered.replace(" ", ""))
        self.assertIn("body, header, .title", rendered)
        self.assertIn("font-family: 'Noto Serif Tamil'", rendered)


if __name__ == "__main__":
    unittest.main()
