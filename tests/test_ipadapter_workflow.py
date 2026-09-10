import json
from pathlib import Path


def test_ipadapter_workflow_has_reference_upload_and_low_vram_canvas():
    path = Path("workflows/selfhost/image_sd15_ipadapter_face_lowvram.json")
    workflow = json.loads(path.read_text(encoding="utf-8"))
    assert workflow["5"]["class_type"] == "IPAdapterUnifiedLoader"
    assert workflow["5"]["inputs"]["preset"] == "PLUS FACE (portraits)"
    assert workflow["6"]["class_type"] == "LoadImage"
    assert "$reference_image.~image!" in workflow["6"]["_meta"]["title"]
    assert workflow["4"]["inputs"]["width"] == 512
    assert workflow["4"]["inputs"]["height"] == 768
    assert workflow["8"]["inputs"]["model"] == ["7", 0]
