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

## Architecture
- **Frontend**: React 19, Tailwind CSS, Phosphor Icons, Framer Motion
- **Backend**: FastAPI, MongoDB, Python
- **Integrations**:
  - Emergent Google OAuth for authentication
  - OpenAI GPT-5.2 for Chinese to Khmer translation (via Emergent LLM Key)
  - OpenAI Whisper for speech-to-text transcription (via Emergent LLM Key)
  - CAMB.AI for real Khmer TTS voices
  - Local file storage (uploads directory)
  - FFmpeg for audio extraction and video merging

## Core Requirements
- [x] Google OAuth login
- [x] Project creation and management
- [x] Video/audio file upload
- [x] Auto-transcription (Whisper)
- [x] Chinese to Khmer translation (GPT-5.2)
- [x] Khmer voice generation (CAMB.AI TTS)
- [x] Video dubbing (merge audio with original video)
- [x] Download dubbed audio/video
- [x] Per-segment custom voice upload
- [x] Actor-level custom voice mapping (Boy/Girl detection)
- [x] Subtitle editor with timestamps

## What's Been Implemented

### Backend
- FastAPI server with /api prefix
- Google OAuth authentication flow
- User and session management (MongoDB)
- Project CRUD operations
- File upload to local storage
- Audio extraction from video (FFmpeg)
- Whisper transcription with segment timestamps
- GPT-5.2 translation endpoint (batch segment translation)
- CAMB.AI TTS audio generation (multi-voice support)
- Video dubbing (audio merge with FFmpeg)
- File download endpoint
- Upload actor voice endpoint (applies to all actor segments)
- Actor detection from transcription segments

### Frontend
- Landing page with dark theme
- Google Sign-In integration
- Dashboard with project list
- Editor with:
  - Video/audio upload
  - Auto-transcribe (Whisper with timestamps)
  - Subtitle table (editable text, timestamps)
  - Translate to Khmer
  - Actors panel (detected speakers with Boy/Girl, AI voice selection, custom voice upload)
  - Audio generation (multi-voice with actor custom voices)
  - Video generation
  - Preview player and download buttons

## Prioritized Backlog

### P0 (Critical)
- [x] Basic dubbing workflow complete
- [x] Actor-level custom voice mapping

### P1 (High Priority)
- [ ] Progress indicators for long operations
- [ ] Batch processing for multiple files

### P2 (Medium Priority)
- [ ] Hardcoded/burned-in subtitle generation on output video
- [ ] Real-time preview of individual segments
- [ ] Voice cloning integration

### P3 (Low Priority)
- [ ] Team collaboration features
- [ ] Usage analytics dashboard
- [ ] API rate limiting

## Key Technical Notes
- CAMB.AI is the ONLY TTS provider that supports native Khmer. Do NOT revert to ElevenLabs or Google TTS.
- FFmpeg is required for audio/video processing
- Emergent LLM Key powers OpenAI GPT-5.2 and Whisper
- Actor voice uploads use Form() parameter for multipart data
