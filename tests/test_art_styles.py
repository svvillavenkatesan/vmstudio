from pixelle_video.art_styles import ART_STYLES, apply_art_style, get_art_style


def test_all_requested_free_prompt_presets_are_available():
    assert len(ART_STYLES) == 27  # Automatic plus the 26 requested styles.
    assert get_art_style("cinematic_art").label_en == "Cinematic Art"
    assert get_art_style("mixed_media").prompt


def test_art_style_is_composed_with_custom_prompt():
    result = apply_art_style("authentic Tamil setting", "paper_cut")
    assert "paper-cut" in result
    assert "authentic Tamil setting" in result


def test_automatic_style_does_not_change_custom_prompt():
    assert apply_art_style("cinematic Tamil visual", "auto") == "cinematic Tamil visual"
