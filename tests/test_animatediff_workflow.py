import json
from pathlib import Path


def test_animatediff_workflow_uses_reference_image_and_low_vram_settings():
    path = Path("workflows/selfhost/video_sd15_animatediff_i2v_lowvram.json")
    workflow = json.loads(path.read_text(encoding="utf-8"))

    assert workflow["2"]["class_type"] == "ADE_LoadAnimateDiffModel"
    assert workflow["2"]["inputs"]["model_name"] == "mm_sd15_v3.safetensors"
    assert workflow["7"]["class_type"] == "LoadImage"
    assert "$reference_image.~image!" in workflow["7"]["_meta"]["title"]
    assert workflow["8"]["inputs"]["width"] == 384
    assert workflow["8"]["inputs"]["height"] == 512
    assert workflow["10"]["inputs"]["amount"] == 8
    assert workflow["14"]["class_type"] == "SaveVideo"
