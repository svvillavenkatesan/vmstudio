from pathlib import Path

from pixelle_video.services.frame_html import HTMLFrameGenerator
from pixelle_video.utils.template_util import (
    get_templates_grouped_by_size_and_type,
    parse_template_size,
)


def test_four_by_three_image_and_video_templates_are_available():
    image_groups = get_templates_grouped_by_size_and_type("image")
    video_groups = get_templates_grouped_by_size_and_type("video")

    assert "1440x1080" in image_groups
    assert "1440x1080" in video_groups
    assert parse_template_size("1440x1080/image_classic_landscape.html") == (1440, 1080)


def test_three_by_four_image_and_video_templates_are_available():
    image_groups = get_templates_grouped_by_size_and_type("image")
    video_groups = get_templates_grouped_by_size_and_type("video")

    assert "1080x1440" in image_groups
    assert "1080x1440" in video_groups
    assert parse_template_size("1080x1440/video_portrait_editorial.html") == (1080, 1440)


def test_new_templates_publish_valid_media_dimensions():
    paths = [
        Path("templates/1440x1080/image_classic_landscape.html"),
        Path("templates/1440x1080/video_classic_landscape.html"),
        Path("templates/1080x1440/image_portrait_editorial.html"),
        Path("templates/1080x1440/video_portrait_editorial.html"),
    ]
    for path in paths:
        width, height = HTMLFrameGenerator(path).get_media_size()
        assert width > 0 and height > 0
