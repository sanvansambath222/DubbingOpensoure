# Khmer Dubbing App - Product Requirements Document

## Original Problem Statement
Build Dubbing China to Khmer using python website following top trending design.

## Supported Output Languages (20 - All Free Edge TTS)
Khmer, Thai, Vietnamese, Korean, Japanese, English, Chinese, Indonesian, Hindi, Spanish, French, Filipino, German, Portuguese, Russian, Arabic, Italian, Malay, Lao, Burmese

## Voice Models Available
1. **Microsoft Edge TTS** - FREE, unlimited, 20+ languages, 2 voices/language
2. **Gemini TTS** - FREE (rate limited), 30 AI voices, high quality, multi-language
3. **Google Cloud TTS** - Premium (~$0.000004/char), 2000+ voices, 40+ languages

## What's Been Implemented
- [x] Google OAuth login, Project CRUD, upload
- [x] Whisper transcription (auto-detect language)
- [x] GPT-5.2 translation to ANY of 20 languages
- [x] Edge TTS voices (male+female per language, free, original voice - no pitch)
- [x] Gemini TTS integration (30 AI voices, free tier)
- [x] Google Cloud TTS integration (2000+ premium voices)
- [x] Voice Picker Modal (3 tabs: Microsoft/Gemini/Google Cloud with preview)
- [x] Per-actor voice model selection (edge/gemini/gcloud per actor)
- [x] Custom voice upload + recording
- [x] Video dubbing, SRT, MP3, batch export, share link
- [x] Parallel TTS (5 at a time), auto-process, queue
- [x] Swiss Light/Dark Theme UI
- [x] Compact actor cards with Boy/Girl distinction + voice model badges (GM/GC)
- [x] Chunked translation (50 segments per batch for long videos)
- [x] Real-time progress bar (segments done, %, elapsed, ETA)
- [x] Output language selector (20 languages in dropdown)
- [x] YouTube voice extraction via yt-dlp (with Node.js JS runtime)
- [x] Auto-fit audio (FFmpeg atempo) for both TTS and custom uploaded voices
- [x] Long video support: background processing, MP3 output, TTS retry (3x)
- [x] 12-hour auto-cleanup for trial user storage
- [x] Delete project with full file cleanup
- [x] Clear All projects button
- [x] Code refactoring: App.js split into 8 components
- [x] Backend refactoring: extracted helpers, Gemini/GCloud TTS functions
- [x] Deployment files (Dockerfile, railway.toml)

## Code Architecture

### Frontend Components
- `App.js` (44 lines) - Router only
- `AuthContext.jsx` - Auth provider, theme toggle
- `LandingPage.jsx` - Landing page
- `Dashboard.jsx` - Project list with CRUD
- `Editor.jsx` - Main editor
- `SharedProject.jsx` - Public shared view
- `EditorWidgets.jsx` - StepProgress, ProcessingOverlay
- `VoicePickerModal.jsx` - 3-tab voice picker (Edge/Gemini/GCloud)
- `constants.js` - API URL, timeouts, languages

### Backend Key Files
- `server.py` - FastAPI with all endpoints
- Key helpers: synthesize_gemini_tts(), synthesize_gcloud_tts(), download_youtube_audio(), assemble_dubbed_video(), fit_audio_to_duration()

## Backlog
### P1
- [ ] Stripe payment for subscription plans (Free/Basic/Pro/Business)

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
