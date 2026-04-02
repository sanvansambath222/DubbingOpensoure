# VoxiDub - PRD

## Problem Statement
Build a video/audio dubbing platform (Any Language to Any Language) with AI transcription, translation, TTS voices, subtitle editing, and AI vocal removal.

## Domain
voxidub.com / dubcambodia.com (DNS setup in progress)

## Architecture
- Frontend: React (modularized components)
- Backend: FastAPI (Python)
- Database: MongoDB
- Storage: Local file storage (/app/uploads)
- Auth: Email/Password + Emergent Google OAuth

## Components
- LandingPage.jsx - Marketing/auth entry
- Dashboard.jsx - Project listing
- Editor.jsx - Main editor with segments, actors, voice controls, extract background
- VoicePickerModal.jsx - Voice selection (Edge TTS only)
- EditorWidgets.jsx - Reusable editor UI pieces
- SharedProject.jsx - Public sharing view
- AuthContext.jsx - Auth state management

## Completed Features
- [x] Video/audio upload and processing
- [x] Whisper transcription (via Emergent LLM key)
- [x] GPT-5.2 translation (via Emergent LLM key)
- [x] Microsoft Edge TTS (free, unlimited)
- [x] Custom voice upload (file + YouTube yt-dlp extraction)
- [x] Long video processing (1h+, MP3 format, 15min timeouts)
- [x] Component refactoring (App.js split into 6 modules)
- [x] Auto-cleanup job (12h project expiry)
- [x] Clear All Projects functionality
- [x] Deployment-ready configs (Dockerfile, railway.toml)
- [x] Per-line speed control (0.5x to 2.0x)
- [x] Per-line speaker reassignment dropdown
- [x] Per-line audio regenerate button
- [x] Actor line filter (click line count to filter segments)
- [x] Background music preservation (extract + mix with dubbed audio)
- [x] Cross-origin Script error suppression
- [x] Bulk DB cleanup optimization (delete_many)
- [x] Deployment health check passed x2
- [x] Email/Password authentication (Register/Login)
- [x] Emergent Google OAuth
- [x] Background Volume slider (0% to 100%)
- [x] Demucs AI vocal removal - FIXED (Python API, removes human voice, keeps music)
- [x] Extract Background Audio button (download music-only file)
- [x] App renamed to VoxiDub

## Removed Features
- Google Cloud TTS (removed per user request)
- Gemini TTS (removed - API quota issues on free tier)

## Upcoming Tasks (P0)
- [ ] Stripe payment integration (Free/Basic/Pro/Business)
- [ ] Usage limits per plan (credits, video counts)

## Future Tasks
- [ ] AI voice cloning & auto lip sync (P1)
- [ ] Mobile-friendly layout (P2)
- [ ] Export different video quality (P2)
- [ ] Team workspace (P3)
- [ ] Multi-language UI (P3)

## 3rd Party Integrations
- OpenAI GPT-5.2 (Translation) - Emergent LLM Key
- OpenAI Whisper (Transcription) - Emergent LLM Key
- Microsoft Edge TTS - Free / No Key
- Demucs AI (Meta) - Local execution via Python API

## Known Issues
- FFmpeg missing on container restart (reinstall via apt-get)
- Demucs uses significant RAM for long audio files

## DB Schema
- projects: {project_id, user_id, title, target_language, status, segments[], actors[], file_type, original_file_path, dubbed_audio_path, dubbed_video_path, bg_audio_path, bg_volume, created_at}
- users: {user_id, email, name, picture, auth_provider, password_hash, created_at}
- user_sessions: {session_token, user_id, expires_at, created_at}

## Technical Notes
- Demucs uses Python API (get_model + apply_model + soundfile) instead of CLI due to torchaudio CUDA dependency issues
- torchaudio 2.11.0+cpu installed but NOT used for I/O (soundfile handles loading/saving)
- scipy used for resampling when audio sample rate doesn't match model's expected rate
