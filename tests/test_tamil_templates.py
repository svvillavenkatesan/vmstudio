import unittest
from pathlib import Path

from pixelle_video.utils.template_util import (
    TAMIL_TEMPLATE_DISPLAY_NAMES,
    get_template_type,
    list_templates_for_size,
    parse_template_size,
)


NEW_TAMIL_TEMPLATES = {
    "image_tamil_festival.html",
    "image_tamil_thirukkural.html",
    "image_tamil_news.html",
    "image_tamil_history.html",
    "image_tamil_product.html",
    "image_tamil_quote_reel.html",
}


class TamilTemplateTests(unittest.TestCase):
    def test_new_templates_are_discoverable(self):
        available = set(list_templates_for_size("1080x1920"))
        self.assertTrue(NEW_TAMIL_TEMPLATES.issubset(available))

    def test_new_templates_require_ai_images(self):
        for name in NEW_TAMIL_TEMPLATES:
            self.assertEqual(get_template_type(name), "image")

    def test_templates_keep_text_outside_generated_image(self):
        template_dir = Path("templates/1080x1920")
        for name in NEW_TAMIL_TEMPLATES:
            html = (template_dir / name).read_text(encoding="utf-8")
            self.assertIn('src="{{image}}"', html)
            self.assertIn("{{title}}", html)
            self.assertIn("{{text}}", html)
            self.assertIn('template:media-width" content="512', html)
            self.assertIn('template:media-height" content="768', html)
            self.assertIn(name, TAMIL_TEMPLATE_DISPLAY_NAMES)

    def test_portrait_dimensions_are_valid(self):
        self.assertEqual(parse_template_size("templates/1080x1920/image_tamil_news.html"), (1080, 1920))


if __name__ == "__main__":
    unittest.main()
