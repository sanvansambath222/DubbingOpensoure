# VoxiDub - PRD

## Problem Statement
Build a video/audio dubbing platform (Any Language to Any Language) with AI transcription, translation, TTS voices, subtitle editing, AI vocal removal, and standalone video/audio tools.

## Architecture
- Frontend: React | Backend: FastAPI | Database: MongoDB | Storage: Local (/app/uploads)
- Auth: Email/Password + Emergent Google OAuth

## Completed Features
- [x] Video/audio upload and processing
- [x] Whisper transcription + GPT-5.2 translation (Emergent LLM Key)
- [x] Microsoft Edge TTS: Piseth (male) + Sreymom (female) - FREE
- [x] Meta MMS Khmer TTS: Meta AI (male) - FREE, open source
- [x] Meta AI (Girl) via pitch shift - FREE
- [x] Custom voice upload (file + YouTube)
- [x] Demucs AI vocal removal (chunked, with progress bar)
- [x] Background Volume slider (0%-100%)
- [x] Extract Background Audio download button
- [x] Background async processing (no proxy timeout)
- [x] Per-line regenerate, speed control, speaker reassignment
- [x] Email/Password auth + Google OAuth
- [x] Auto-cleanup job, Clear All Projects
- [x] App renamed to VoxiDub
- [x] SpeechBrain ECAPA-TDNN audio-based speaker diarization
- [x] Autocorrelation F0 pitch analysis for gender detection
- [x] GPT role detection runs in background (non-blocking)
- [x] SpeechBrain model preloaded at startup
- [x] FFmpeg auto-install at startup
- [x] Double-click guard for auto-process
- [x] MMS speed adjusted to 0.9x base
- [x] 7 Standalone Tools page (Add Subtitles, Translate, Trim, AI Clips, TTS, Resize, Convert)

## Voice Defaults (Auto-Process)
| Gender | Voice | Provider |
|--------|-------|----------|
| Boy | Meta AI (Boy) | Meta MMS (mms_khmer) |
| Girl | Sreymom (Girl) | Edge TTS (sophea) |

## Standalone Tools
| Tool | Backend | Cost |
|------|---------|------|
| Add Subtitles | FFmpeg | FREE |
| Translate | GPT-5.2 | Emergent Key |
| Trim Video | FFmpeg | FREE |
| AI Clips | Whisper + GPT-5.2 + FFmpeg | Emergent Key |
| Text to Speech | Meta MMS + Edge TTS | FREE |
| Resize Video | FFmpeg | FREE |
| Convert | FFmpeg | FREE |

## Upcoming Tasks (P0)
- [ ] Stripe payment integration (Free/Basic/Pro/Business)
- [ ] Usage limits per plan (credits, video counts)

## Future Tasks
- [ ] AI voice cloning (P1)
- [ ] Auto lip sync (P1)
- [ ] Mobile-friendly layout (P2)
- [ ] Export different video quality (P2)
- [ ] Team workspace (P3)

## 3rd Party Integrations
- OpenAI GPT-5.2 + Whisper (Emergent LLM Key)
- Microsoft Edge TTS (Free)
- Meta MMS TTS facebook/mms-tts-khm (Free, local)
- SpeechBrain ECAPA-TDNN (Free, local, /root/.cache/spkrec-ecapa)
- Demucs AI vocal removal (Free, local Python API)

## Known Issues
- FFmpeg missing on container restart → auto-installs at startup now
- Disk space: ML models use significant space, monitor /root/ partition
- MongoDB may crash if disk full (ENOSPC)
