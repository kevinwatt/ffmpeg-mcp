"""Pytest configuration and fixtures."""

import asyncio
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_video(temp_dir: Path) -> Path:
    """Create a sample video file using FFmpeg."""
    output_path = temp_dir / "sample.mp4"

    # Create a 2-second test video with color bars
    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", "testsrc=duration=2:size=320x240:rate=30",
        "-f", "lavfi",
        "-i", "sine=frequency=440:duration=2",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-y",
        str(output_path),
    ]

    import subprocess
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        pytest.skip("FFmpeg not available or failed to create test video")

    return output_path


@pytest.fixture
def sample_audio(temp_dir: Path) -> Path:
    """Create a sample audio file using FFmpeg."""
    output_path = temp_dir / "sample.mp3"

    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", "sine=frequency=440:duration=2",
        "-c:a", "libmp3lame",
        "-y",
        str(output_path),
    ]

    import subprocess
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        pytest.skip("FFmpeg not available or failed to create test audio")

    return output_path
