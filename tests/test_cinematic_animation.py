import math
import wave

import ffmpeg
from PIL import Image

from pixelle_video.services.video import VideoService


def _silent_wav(path, duration=0.6, rate=16000):
    frames = b"\x00\x00" * math.ceil(duration * rate)
    with wave.open(str(path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(rate)
        output.writeframes(frames)


def test_cinematic_segment_stops_at_its_own_audio_duration(tmp_path):
    image = tmp_path / "scene.png"
    audio = tmp_path / "scene.wav"
    output = tmp_path / "segment.mp4"
    Image.new("RGB", (360, 640), (220, 120, 40)).save(image)
    _silent_wav(audio)

    VideoService().create_video_from_image(
        str(image), str(audio), str(output), fps=10,
        animation="cinematic", animation_variant=2,
    )

    probe = ffmpeg.probe(str(output))
    duration = float(probe["format"]["duration"])
    video = next(stream for stream in probe["streams"] if stream["codec_type"] == "video")
    assert 0.55 <= duration <= 0.75
    assert (int(video["width"]), int(video["height"])) == (360, 640)


def test_four_cinematic_segments_concatenate_in_order(tmp_path):
    service = VideoService()
    segments = []
    for index, colour in enumerate(((220, 30, 30), (30, 220, 30), (30, 30, 220), (220, 180, 30))):
        image = tmp_path / f"scene_{index}.png"
        audio = tmp_path / f"scene_{index}.wav"
        segment = tmp_path / f"segment_{index}.mp4"
        Image.new("RGB", (360, 640), colour).save(image)
        _silent_wav(audio)
        service.create_video_from_image(
            str(image), str(audio), str(segment), fps=10,
            animation="cinematic", animation_variant=index,
        )
        segments.append(str(segment))

    final = tmp_path / "final.mp4"
    service.concat_videos(segments, str(final))
    duration = float(ffmpeg.probe(str(final))["format"]["duration"])
    assert 2.2 <= duration <= 3.0
