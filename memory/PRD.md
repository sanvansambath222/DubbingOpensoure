# Khmer Dubbing App - Product Requirements Document

## Original Problem Statement
Build Dubbing China to Khmer using python website following top trending design.

## Supported Output Languages (20 - All Free Edge TTS)
Khmer, Thai, Vietnamese, Korean, Japanese, English, Chinese, Indonesian, Hindi, Spanish, French, Filipino, German, Portuguese, Russian, Arabic, Italian, Malay, Lao, Burmese

## What's Been Implemented
- [x] Google OAuth login, Project CRUD, upload
- [x] Whisper transcription (auto-detect language)
- [x] GPT-5.2 translation to ANY of 20 languages
- [x] Edge TTS voices (male+female per language, free)
- [x] Per-actor voice, pitch, age detection
- [x] Custom voice upload + recording
- [x] Video dubbing, SRT, MP3, batch export, share link
- [x] Parallel TTS (5 at a time), auto-process, queue
- [x] Swiss Light/Dark Theme UI
- [x] Compact actor cards with Boy/Girl distinction
- [x] **Chunked translation** (50 segments per batch for long videos)
- [x] **Real-time progress bar** (segments done, %, elapsed, ETA)
- [x] **Output language selector** (20 languages in dropdown)

## Key Technical Notes
- DO NOT re-add SSML/Emotion TTS
- EDGE_TTS_VOICES dict in server.py maps lang->gender->voice
- target_language stored in project doc, defaults to "km"
- Translation chunks: 50 segments per GPT call
- Progress tracked via queue_status dict, polled every 1.5s
- /api/languages endpoint REMOVED (languages in frontend only)

## Backlog
### P2
- [ ] AI voice cloning
- [ ] Auto lip sync
- [ ] Drag to adjust timing
- [ ] Export different video quality
- [ ] Mobile friendly layout

### P3
- [ ] Team workspace
- [ ] Multi-language UI
- [ ] Waveform timeline
