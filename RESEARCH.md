# FFmpeg-MCP Project Research Report

## Table of Contents

1. [Reference Project Analysis: yt-dlp-mcp](#1-reference-project-analysis-yt-dlp-mcp)
2. [Existing FFmpeg MCP Implementations Comparison](#2-existing-ffmpeg-mcp-implementations-comparison)
3. [Feature Comparison Table](#3-feature-comparison-table)
4. [Technical Recommendations](#4-technical-recommendations)
5. [Project Structure Planning](#5-project-structure-planning)

---

## 1. Reference Project Analysis: yt-dlp-mcp

> Source: `/home/kevin/project/yt-dlp-mcp`

### 1.1 Project Structure

```
yt-dlp-mcp/
├── src/
│   ├── index.mts                    # MCP server core
│   ├── config.ts                    # Centralized configuration
│   └── modules/
│       ├── video.ts                 # Video download
│       ├── audio.ts                 # Audio extraction
│       ├── subtitle.ts              # Subtitle features
│       ├── search.ts                # Search functionality
│       ├── metadata.ts              # Metadata handling
│       ├── comments.ts              # Comment extraction
│       └── utils.ts                 # Shared utilities
├── src/__tests__/                   # Jest test suite
├── docs/                            # Detailed documentation
├── README.md
├── CLAUDE.md
├── CHANGELOG.md
├── package.json
├── tsconfig.json
└── jest.config.mjs
```

### 1.2 Key Design Patterns

| Feature | Description |
|---------|-------------|
| **Tool Prefix** | All tools use `ytdlp_` prefix to avoid naming conflicts |
| **Zod Validation** | Runtime parameter validation using Zod |
| **Modular Design** | Functions separated by responsibility into modules |
| **Centralized Config** | Environment variables managed by config.ts |
| **JSDoc Comments** | Complete function documentation with examples |

### 1.3 MCP Implementation Highlights

```typescript
// Tool registration pattern
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools: [...] };
});

// Tool execution pattern
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const params = Schema.parse(request.params.arguments);
  const result = await handler(params);
  return { content: [{ type: "text", text: result }] };
});
```

---

## 2. Existing FFmpeg MCP Implementations Comparison

### 2.1 egoist/ffmpeg-mcp

| Item | Details |
|------|---------|
| **GitHub** | https://github.com/egoist/ffmpeg-mcp |
| **Language** | TypeScript (98.8%) |
| **Runtime** | Bun / npx |
| **Stars** | 119 |
| **License** | MIT |

**Features:**
- Minimalist design with only two core files (main.ts, tools.ts)
- Run with `npx -y ffmpeg-mcp`
- Supports `FFMPEG_PATH` environment variable
- Still expanding functionality

**Pros:** Lightweight, easy to use
**Cons:** Limited features, incomplete documentation

---

### 2.2 misbahsy/video-audio-mcp

| Item | Details |
|------|---------|
| **GitHub** | https://github.com/misbahsy/video-audio-mcp |
| **Language** | Python |
| **Framework** | FastMCP |
| **Stars** | 52 |
| **License** | MIT |

**Supported Tools (27):**

| Category | Count | Features |
|----------|-------|----------|
| Video Processing | 9 | Format conversion, resolution, codecs, frame rate |
| Audio Processing | 9 | Format conversion, bitrate, sample rate, channels |
| Creative Tools | 5 | Subtitles, text overlay, image overlay, B-Roll, transitions |
| Advanced Editing | 4 | Merge, speed change, silence removal, health check |

**Features:**
- Most comprehensive functionality
- Uses FastMCP framework
- Includes 25+ test cases
- Detailed use case documentation

**Pros:** Feature-rich, well-tested, detailed documentation
**Cons:** Many dependencies, relatively complex

---

### 2.3 sworddut/mcp-ffmpeg-helper

| Item | Details |
|------|---------|
| **GitHub** | https://github.com/sworddut/mcp-ffmpeg-helper |
| **Language** | TypeScript |
| **Runtime** | Node.js v14+ |
| **License** | MIT |

**Supported Tools:**
1. `get_video_info` - Get video information
2. Format conversion
3. Audio extraction
4. Video synthesis (from image sequences)
5. Time trimming
6. Watermark addition
7. Frame extraction

**Project Structure:**
```
src/
├── index.ts              # MCP server entry
├── utils/
│   ├── file.ts          # File operations
│   └── ffmpeg.ts        # FFmpeg utilities
└── tools/
    ├── definitions.ts    # Tool definitions
    └── handlers.ts       # Handler functions
```

**Pros:** Clean structure, modular design
**Cons:** Medium functionality, less maintenance

---

### 2.4 video-creator/ffmpeg-mcp

| Item | Details |
|------|---------|
| **GitHub** | https://github.com/video-creator/ffmpeg-mcp |
| **Language** | Python (100%) |
| **Package Manager** | uv |
| **Stars** | 109 |
| **License** | MIT |

**Supported Tools:**

| Tool | Function |
|------|----------|
| `find_video_path` | Recursively search for video files |
| `get_video_info` | Extract video information |
| `clip_video` | Trim video |
| `concat_videos` | Merge videos |
| `play_video` | Play video |
| `overlay_video` | Video overlay |
| `scale_video` | Adjust resolution |
| `extract_frames_from_video` | Extract frames |

**Features:**
- Focus on core functionality
- Uses modern Python toolchain (uv)
- Currently macOS only

**Pros:** Clean design, uses uv
**Cons:** Platform limitations, limited features

---

## 3. Feature Comparison Table

| Feature | egoist | misbahsy | sworddut | video-creator |
|---------|:------:|:--------:|:--------:|:-------------:|
| **Basic Features** |||||
| Format Conversion | ✅ | ✅ | ✅ | ❌ |
| Video Info | ❌ | ✅ | ✅ | ✅ |
| Trim/Cut | ❌ | ✅ | ✅ | ✅ |
| Merge Videos | ❌ | ✅ | ❌ | ✅ |
| **Audio Processing** |||||
| Audio Extraction | ❌ | ✅ | ✅ | ❌ |
| Audio Conversion | ❌ | ✅ | ❌ | ❌ |
| Silence Removal | ❌ | ✅ | ❌ | ❌ |
| **Video Processing** |||||
| Resolution Adjustment | ❌ | ✅ | ❌ | ✅ |
| Codec Settings | ❌ | ✅ | ✅ | ❌ |
| Frame Rate Adjustment | ❌ | ✅ | ❌ | ❌ |
| Speed Change | ❌ | ✅ | ❌ | ❌ |
| **Advanced Features** |||||
| Add Subtitles | ❌ | ✅ | ❌ | ❌ |
| Watermark | ❌ | ✅ | ✅ | ❌ |
| Text Overlay | ❌ | ✅ | ❌ | ❌ |
| Image Overlay | ❌ | ✅ | ❌ | ✅ |
| Transitions | ❌ | ✅ | ❌ | ❌ |
| Frame Extraction | ❌ | ❌ | ✅ | ✅ |
| **Technical Aspects** |||||
| Language | TS | Python | TS | Python |
| Tests | ❌ | ✅ | ❌ | ❌ |
| Documentation | Basic | Complete | Medium | Basic |

---

## 4. Technical Recommendations

### 4.1 Language Choice: Python

**Reasons:**
1. User explicitly requested Python
2. Mature Python ecosystem for FFmpeg (ffmpeg-python, pymediainfo)
3. Easy integration with AI/ML tools
4. misbahsy and video-creator provide good Python references

### 4.2 Framework Selection

| Option | Pros | Cons |
|--------|------|------|
| **FastMCP** | Simplified development, community support | Extra dependency |
| **Native MCP SDK** | High control, fewer dependencies | More development work |

**Recommendation:** Use FastMCP for rapid development

### 4.3 Package Management

| Option | Pros | Cons |
|--------|------|------|
| **uv** | Modern, fast, lock files | Newer |
| **pip** | Wide support | Slower |
| **poetry** | Feature complete | Complex |

**Recommendation:** Use **uv**, consistent with video-creator/ffmpeg-mcp

### 4.4 Core Dependencies

```toml
[project]
dependencies = [
    "mcp",              # MCP SDK
]
```

---

## 5. Project Structure Planning

### 5.1 Recommended Directory Structure

```
ffmpeg-mcp/
├── src/
│   └── ffmpeg_mcp/
│       ├── __init__.py
│       ├── __main__.py          # Entry point
│       ├── server.py            # MCP server core
│       ├── config.py            # Configuration management
│       └── tools/
│           ├── __init__.py
│           ├── info.py          # Video info tool
│           ├── convert.py       # Format conversion tool
│           ├── trim.py          # Trim tool
│           ├── merge.py         # Merge tool
│           ├── audio.py         # Audio processing tool
│           └── frames.py        # Frame extraction tool
├── tests/                       # pytest tests
│   ├── __init__.py
│   ├── test_info.py
│   ├── test_convert.py
│   └── ...
├── README.md
├── CLAUDE.md
├── pyproject.toml
├── uv.lock
└── .gitignore
```

### 5.2 Tool Naming Convention

Following yt-dlp-mcp's prefix convention:

```python
# All tools prefixed with ffmpeg_
tools = [
    "ffmpeg_get_info",
    "ffmpeg_convert",
    "ffmpeg_trim",
    "ffmpeg_merge",
    "ffmpeg_extract_audio",
    "ffmpeg_compress",
    "ffmpeg_extract_frames",
]
```

### 5.3 Implementation Priority

Sorted by usage frequency and implementation complexity:

| Priority | Tool | Description |
|:--------:|------|-------------|
| P0 | `ffmpeg_get_info` | Get video/audio metadata |
| P0 | `ffmpeg_convert` | Format conversion |
| P0 | `ffmpeg_compress` | Video compression |
| P0 | `ffmpeg_trim` | Trim/cut |
| P0 | `ffmpeg_extract_audio` | Extract audio track |
| P1 | `ffmpeg_merge` | Merge videos |
| P1 | `ffmpeg_extract_frames` | Extract frames |

---

## 6. References

- [egoist/ffmpeg-mcp](https://github.com/egoist/ffmpeg-mcp) - TypeScript lightweight implementation
- [misbahsy/video-audio-mcp](https://github.com/misbahsy/video-audio-mcp) - Python full implementation
- [sworddut/mcp-ffmpeg-helper](https://github.com/sworddut/mcp-ffmpeg-helper) - TypeScript modular implementation
- [video-creator/ffmpeg-mcp](https://github.com/video-creator/ffmpeg-mcp) - Python simple implementation
- [yt-dlp-mcp](https://github.com/kevinwatt/yt-dlp-mcp) - Reference style source
