# Khmer Dubbing App - Product Requirements Document

## Original Problem Statement
Build Dubbing China to Khmer using python website following top trending design (HeyGen-inspired).

## User Choices
- Upload video/audio -> Get Khmer dubbed output
- Auto-transcribe using OpenAI Whisper (auto-detect language)
- Translation using OpenAI GPT-5.2 (any language to Khmer)
- Khmer TTS using Microsoft Edge TTS (free, native Khmer voices)
- Google social login (Emergent-managed)
- Output: MP4 video, WAV audio, MP3 audio, SRT subtitles
- Auto-detect actors (Boy/Girl) and upload custom voice per actor
- Share dubbed project via public link

## Architecture
- **Frontend**: React 19, Tailwind CSS, Phosphor Icons, Framer Motion
- **Backend**: FastAPI, MongoDB, Python
- **Integrations**:
  - Emergent Google OAuth for authentication
  - OpenAI GPT-5.2 for translation (via Emergent LLM Key)
  - OpenAI Whisper for speech-to-text with auto language detection (via Emergent LLM Key)
  - Microsoft Edge TTS for real Khmer voices (free, no key needed)
  - FFmpeg for audio extraction, video merging, MP3 conversion

## What's Been Implemented
- [x] Google OAuth login
- [x] Project creation and management (CRUD)
- [x] Video/audio file upload
- [x] Auto-transcription (Whisper) with auto language detection
- [x] Speaker detection via GPT (role + gender from dialogue context)
- [x] Any language to Khmer translation (GPT-5.2)
- [x] Khmer voice generation (Edge TTS - Piseth/Sreymom neural voices)
- [x] Video dubbing (merge audio with original video)
- [x] Download: WAV audio, MP4 video, MP3 audio, SRT subtitles
- [x] Actor-level custom voice mapping
- [x] Per-segment custom voice upload
- [x] Subtitle editor with timestamps + Length column
- [x] Auto speaking time per actor
- [x] Download Script (.txt) per actor (paged for long videos)
- [x] Built-in voice recorder
- [x] Original video preview + side-by-side compare
- [x] TTS speed slider (-10% to +15%)
- [x] Single-line audio preview (Play button per row)
- [x] Step progress bar
- [x] Share project via public link (with video, audio, SRT download)
- [x] Shared project page (public, no auth required)
- [x] Improved dashboard with dates, segment counts, actor counts, language badge
- [x] Burned-in subtitles option (off by default)

## Prioritized Backlog

### P1 (High Priority)
- [ ] Progress percentage during long operations

### P2 (Medium Priority)
- [ ] Bulk edit segments (select many, change all at once)
- [ ] Drag to adjust segment timing
- [ ] Export different video quality (720p, 1080p)
- [ ] Multi-language input improvements (Thai, Vietnamese, Korean specific prompts)

### P3 (Low Priority)
- [ ] AI voice cloning (needs paid API like ElevenLabs)
- [ ] Auto lip sync (complex AI model needed)
- [ ] Team workspace / collaboration
- [ ] Usage analytics dashboard
- [ ] Waveform timeline visualization

## Key Technical Notes
- Edge TTS voices: km-KH-PisethNeural (Male), km-KH-SreymomNeural (Female)
- DO NOT use pitch analysis for gender detection - use GPT dialogue analysis
- Custom audio hierarchy: Segment Custom > Actor Custom > AI TTS
- Whisper auto-detects language (removed hardcoded "zh")
- Share system: share_token stored in project doc, public endpoints at /api/shared/{token}
