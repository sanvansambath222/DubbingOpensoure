# VoxiDub - PRD

## Problem Statement
Build a video/audio dubbing platform (Any Language to Any Language) with AI transcription, translation, TTS voices, subtitle editing, and AI vocal removal.

## Architecture
- Frontend: React | Backend: FastAPI | Database: MongoDB | Storage: Local (/app/uploads)
- Auth: Email/Password + Emergent Google OAuth

## Completed Features
- [x] Video/audio upload and processing
- [x] Whisper transcription + GPT-5.2 translation (Emergent LLM Key)
- [x] Microsoft Edge TTS: Piseth (male) + Sreymom (female) - FREE
- [x] Meta MMS Khmer TTS: Meta AI (male) - FREE, open source
- [x] KLEA Khmer TTS: KLEA (male) - FREE, open source, word-by-word
- [x] Custom voice upload (file + YouTube)
- [x] Demucs AI vocal removal (chunked, with progress bar)
- [x] Background Volume slider (0%-100%)
- [x] Extract Background Audio download button
- [x] Background async processing (no proxy timeout)
- [x] Per-line regenerate, speed control, speaker reassignment
- [x] Email/Password auth + Google OAuth
- [x] Auto-cleanup job, Clear All Projects
- [x] App renamed to VoxiDub

## Khmer Voice Options
| Voice | Provider | Type | Quality |
|-------|----------|------|---------|
| Piseth (Boy) | Edge TTS | Full sentence | Medium (robot-like) |
| Sreymom (Girl) | Edge TTS | Full sentence | Medium (robot-like) |
| Meta AI (Boy) | Meta MMS | Full sentence | Good (AI) |
| KLEA (Boy) | KLEA/VITS | Word-by-word | Unique (choppy) |

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
- Meta MMS TTS facebook/mms-tts-khm (Free, local, /root/.cache/mms-tts-khm)
- KLEA TTS seanghay/KLEA (Free, local, /root/.cache/klea/G_60000.pth)
- Demucs AI vocal removal (Free, local Python API)

## Known Issues
- FFmpeg missing on container restart (reinstall via apt-get)
- KLEA requires G_60000.pth in /root/.cache/klea/ (must be re-downloaded on restart)
- HuggingFace rate limiting (use hf-mirror.com as fallback)
