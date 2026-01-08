# FFmpeg MCP - TODO

## Phase 1: Project Setup
- [x] Initialize git repository
- [x] Create .gitignore
- [x] Create pyproject.toml
- [x] Create project directory structure
- [x] Create .claude/skills/mcp-builder/SKILL.md

## Phase 2: Core Implementation
- [x] Create config.py (configuration management)
- [x] Create server.py (MCP server core)

## Phase 3: Tool Implementation

### P0 - Core Features
- [x] `ffmpeg_get_info` - Get video/audio metadata
- [x] `ffmpeg_convert` - Format conversion (with scale option)
- [x] `ffmpeg_compress` - Video compression (with scale option)
- [x] `ffmpeg_trim` - Trim video segments
- [x] `ffmpeg_extract_audio` - Extract audio track

### P1 - Secondary Features
- [x] `ffmpeg_merge` - Merge/concatenate videos
- [x] `ffmpeg_extract_frames` - Extract frames as images

## Phase 4: Documentation and Testing
- [x] Create README.md
- [x] Create CLAUDE.md
- [x] Create test cases (26 tests all passed)

## Tool Specifications Summary

| Tool | Input | Output |
|------|-------|--------|
| `ffmpeg_get_info` | Video path | JSON metadata (duration, resolution, codecs, etc.) |
| `ffmpeg_convert` | Path, target format, scale (optional) | Converted file path |
| `ffmpeg_compress` | Path, quality, scale (optional) | Compressed file path |
| `ffmpeg_trim` | Path, start time, end time | Trimmed file path |
| `ffmpeg_extract_audio` | Video path, audio format | Audio file path |
| `ffmpeg_merge` | Video path list | Merged file path |
| `ffmpeg_extract_frames` | Video path, interval/count | Frames directory path |
