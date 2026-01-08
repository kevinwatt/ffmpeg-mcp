# FFmpeg MCP Server

An MCP (Model Context Protocol) server that provides video and audio processing capabilities through FFmpeg.

## Installation

```bash
uv sync
```

## Usage

Run the MCP server:

```bash
uv run ffmpeg-mcp
```

### Configuration

Configure via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `FFMPEG_PATH` | Path to ffmpeg binary | `ffmpeg` |
| `FFPROBE_PATH` | Path to ffprobe binary | `ffprobe` |
| `FFMPEG_OUTPUT_DIR` | Default output directory | `~/Downloads` |

## Available Tools

### ffmpeg_get_info

Get video/audio file metadata including duration, resolution, codecs, and stream information.

### ffmpeg_convert

Convert video/audio to a different format with optional resolution scaling and codec selection.

### ffmpeg_compress

Compress video files to reduce file size with configurable quality and encoding presets.

### ffmpeg_trim

Trim video to extract a specific segment by specifying start time and end time or duration.

### ffmpeg_extract_audio

Extract audio track from a video file in various formats (mp3, aac, wav, flac, ogg, opus).

### ffmpeg_merge

Concatenate multiple video files into one.

### ffmpeg_extract_frames

Extract frames from a video as images at specified intervals or count.

## Development

```bash
# Run tests
uv run pytest

# Type checking
uv run mypy src/

# Linting
uv run ruff check src/
```

## License

MIT
