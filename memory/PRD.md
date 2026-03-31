# Khmer Dubbing App - Product Requirements Document

## Original Problem Statement
Build Dubbing China to Khmer using python website following top trending design (HeyGen-inspired).

## User Choices
- Upload video/audio -> Get Khmer dubbed output
- Auto-transcribe using OpenAI Whisper
- Translation using OpenAI GPT-5.2
- Khmer TTS using CAMB.AI (native Khmer voices)
- Google social login (Emergent-managed)
- Output: Both audio and video options
- Auto-detect actors (Boy/Girl) and upload ONE custom voice per actor
- Simple actor labels: "Man" / "Woman"
- No subtitles on video by default

## Architecture
- **Frontend**: React 19, Tailwind CSS, Phosphor Icons, Framer Motion
- **Backend**: FastAPI, MongoDB, Python
- **Integrations**:
  - Emergent Google OAuth for authentication
  - OpenAI GPT-5.2 for Chinese to Khmer translation (via Emergent LLM Key)
  - OpenAI Whisper for speech-to-text transcription (via Emergent LLM Key)
  - CAMB.AI for real Khmer TTS voices
  - FFmpeg for audio extraction and video merging

## What's Been Implemented
- [x] Google OAuth login
- [x] Project creation and management (CRUD)
- [x] Video/audio file upload
- [x] Auto-transcription (Whisper) with speaker detection
- [x] Chinese to Khmer translation (GPT-5.2)
- [x] Khmer voice generation (CAMB.AI TTS)
- [x] Video dubbing (merge audio with original video)
- [x] Download dubbed audio/video
- [x] Actor-level custom voice mapping (Man/Woman labels)
- [x] Per-segment custom voice upload
- [x] Subtitle editor with timestamps + Length column
- [x] Auto speaking time per actor (calculated from timestamps)
- [x] Download Script (.txt) per actor
- [x] "Say:" text hints in Add Voice column
- [x] Recording recommendation per segment
- [x] Burned-in subtitles option (off by default)
- [x] Built-in voice recorder (record in browser)
- [x] Original video preview in editor
- [x] Side-by-side compare (original vs dubbed)
- [x] Step progress bar (Upload > Detect > Translate > Audio > Video)
- [x] Processing overlay with spinner

## Prioritized Backlog

### P1 (High Priority)
- [ ] Improve speaker detection accuracy
- [ ] Progress percentage during long operations

### P2 (Medium Priority)
- [ ] Multi-language support (Thai, Vietnamese, Japanese to Khmer)
- [ ] Batch upload multiple videos

### P3 (Low Priority)
- [ ] Team collaboration features
- [ ] Usage analytics dashboard

## Key Technical Notes
- CAMB.AI is the ONLY TTS provider that supports native Khmer. Do NOT revert to ElevenLabs or Google TTS.
- FFmpeg is required for audio/video processing
- Emergent LLM Key powers OpenAI GPT-5.2 and Whisper
- Actor voice uploads use Form() parameter for multipart data
- Voice recorder uses MediaRecorder API (audio/webm format)
