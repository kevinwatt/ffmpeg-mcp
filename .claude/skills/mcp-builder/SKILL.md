# FFmpeg MCP Server Development Guide

## Overview

This skill guides the development of `ffmpeg-mcp`, an MCP server that provides video and audio processing capabilities through FFmpeg.

---

## Project Specifications

### Technology Stack
- **Language**: Python 3.10+
- **Framework**: FastMCP (from mcp package)
- **Package Manager**: uv
- **CLI Tool**: FFmpeg / FFprobe

### Tool Naming Convention
All tools use `ffmpeg_` prefix to avoid conflicts with other MCP servers.

---

## Tools to Implement

### P0 - Core Tools (Must Have)

| Tool | Description | Parameters |
|------|-------------|------------|
| `ffmpeg_get_info` | Get video/audio metadata | `file_path` |
| `ffmpeg_convert` | Convert format (with optional scale) | `file_path`, `output_format`, `scale?`, `video_codec?`, `audio_codec?` |
| `ffmpeg_compress` | Compress video (with optional scale) | `file_path`, `quality`, `scale?`, `preset?` |
| `ffmpeg_trim` | Trim video segment | `file_path`, `start_time`, `end_time?`, `duration?` |
| `ffmpeg_extract_audio` | Extract audio track | `file_path`, `audio_format`, `bitrate?` |

### P1 - Secondary Tools (Nice to Have)

| Tool | Description | Parameters |
|------|-------------|------------|
| `ffmpeg_merge` | Concatenate videos | `file_paths`, `output_path?` |
| `ffmpeg_extract_frames` | Extract frames as images | `file_path`, `interval?`, `count?`, `format?` |

---

## Implementation Guidelines

### 1. Project Structure

```
ffmpeg-mcp/
├── src/ffmpeg_mcp/
│   ├── __init__.py
│   ├── __main__.py
│   ├── server.py          # MCP server core
│   ├── config.py          # Configuration
│   └── tools/
│       ├── __init__.py
│       ├── info.py
│       ├── convert.py
│       ├── compress.py
│       ├── trim.py
│       ├── audio.py
│       ├── merge.py
│       └── frames.py
├── tests/
├── pyproject.toml
├── README.md
└── CLAUDE.md
```

### 2. FastMCP Pattern

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ffmpeg-mcp")

@mcp.tool()
async def ffmpeg_get_info(file_path: str) -> str:
    """Get video/audio file information.

    Args:
        file_path: Path to the media file

    Returns:
        JSON string with media metadata
    """
    # Implementation
    pass
```

### 3. FFmpeg Execution Pattern

```python
import asyncio
import json

async def run_ffprobe(file_path: str) -> dict:
    """Run ffprobe and return parsed JSON output."""
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {stderr.decode()}")
    return json.loads(stdout.decode())
```

### 4. Error Handling

Provide actionable error messages:

```python
class FFmpegError(Exception):
    """FFmpeg execution error with helpful message."""
    pass

def validate_file(file_path: str) -> Path:
    """Validate file exists and is readable."""
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        raise FFmpegError(f"File not found: {file_path}")
    if not path.is_file():
        raise FFmpegError(f"Not a file: {file_path}")
    return path
```

### 5. Tool Annotations

```python
@mcp.tool(
    annotations={
        "readOnlyHint": True,      # For get_info
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
async def ffmpeg_get_info(file_path: str) -> str:
    ...
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FFMPEG_PATH` | Path to ffmpeg binary | `ffmpeg` |
| `FFPROBE_PATH` | Path to ffprobe binary | `ffprobe` |
| `FFMPEG_OUTPUT_DIR` | Default output directory | `~/Downloads` |

---

## Quality Checklist

Before completion, verify:

- [ ] All tools have clear docstrings with Args and Returns
- [ ] Input validation for all parameters
- [ ] Proper async/await for subprocess calls
- [ ] Actionable error messages
- [ ] File path expansion (~, relative paths)
- [ ] Output file naming convention
- [ ] Progress indication for long operations (if supported)

---

## Reference

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [FFprobe Documentation](https://ffmpeg.org/ffprobe.html)
