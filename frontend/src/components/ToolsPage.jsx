import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Subtitles, Translate, Scissors, FilmSlate, SpeakerHigh,
  ArrowsOut, ArrowsClockwise, ArrowLeft, UploadSimple, DownloadSimple,
  SpinnerGap, Check, X, Play, Pause, MicrophoneStage
} from "@phosphor-icons/react";
import { useAuth, ThemeToggle } from "./AuthContext";
import { API } from "./constants";
import axios from "axios";
import { toast } from "sonner";

const TOOLS = [
  { id: "subtitles", name: "Add Subtitles", desc: "Burn subtitles into video from SRT file", icon: Subtitles, color: "bg-rose-500" },
  { id: "translate", name: "Translate", desc: "Translate SRT subtitles to any language", icon: Translate, color: "bg-violet-500" },
  { id: "trim", name: "Trim Video", desc: "Cut video by start & end time", icon: Scissors, color: "bg-amber-500" },
  { id: "ai-clips", name: "AI Clips", desc: "Auto-create short clips from long video", icon: FilmSlate, color: "bg-cyan-500" },
  { id: "tts", name: "Text to Speech", desc: "Type text and get Khmer audio", icon: SpeakerHigh, color: "bg-emerald-500" },
  { id: "resize", name: "Resize Video", desc: "Change video size: 16:9, 9:16, 1:1", icon: ArrowsOut, color: "bg-blue-500" },
  { id: "convert", name: "Convert", desc: "Convert video format: MP4, MOV, AVI, WebM", icon: ArrowsClockwise, color: "bg-orange-500" },
];

// ---- Subtitles Tool ----
const SubtitlesTool = ({ token, d }) => {
  const [video, setVideo] = useState(null);
  const [srt, setSrt] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [fontSize, setFontSize] = useState(24);
  const [fontColor, setFontColor] = useState("white");
  const [position, setPosition] = useState("bottom");

  const handleProcess = async () => {
    if (!video || !srt) return toast.error("Upload video and SRT file");
    setProcessing(true);
    try {
      const fd = new FormData();
      fd.append("video", video);
      fd.append("srt", srt);
      fd.append("font_size", fontSize);
      fd.append("font_color", fontColor);
      fd.append("position", position);
      const r = await axios.post(`${API}/tools/add-subtitles`, fd, {
        headers: { Authorization: `Bearer ${token}` }, timeout: 600000
      });
      setResult(r.data.download_url);
      toast.success("Subtitles burned!");
    } catch (e) { toast.error(e.response?.data?.detail || "Failed"); }
    finally { setProcessing(false); }
  };

  return (
    <div className="space-y-4">
      <div>
        <label className={`block text-sm font-medium mb-1 ${d?'text-zinc-300':'text-zinc-700'}`}>Video File</label>
        <input type="file" accept="video/*" onChange={e => setVideo(e.target.files[0])}
          className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} data-testid="subtitles-video-input" />
      </div>
      <div>
        <label className={`block text-sm font-medium mb-1 ${d?'text-zinc-300':'text-zinc-700'}`}>SRT Subtitle File</label>
        <input type="file" accept=".srt,.vtt,.ass" onChange={e => setSrt(e.target.files[0])}
          className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} data-testid="subtitles-srt-input" />
      </div>
      <div className="grid grid-cols-3 gap-3">
        <div>
          <label className={`block text-xs mb-1 ${d?'text-zinc-400':'text-zinc-600'}`}>Font Size</label>
          <input type="number" value={fontSize} onChange={e => setFontSize(e.target.value)} min={12} max={72}
            className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} />
        </div>
        <div>
          <label className={`block text-xs mb-1 ${d?'text-zinc-400':'text-zinc-600'}`}>Color</label>
          <select value={fontColor} onChange={e => setFontColor(e.target.value)}
            className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`}>
            <option value="white">White</option>
            <option value="yellow">Yellow</option>
            <option value="green">Green</option>
            <option value="cyan">Cyan</option>
          </select>
        </div>
        <div>
          <label className={`block text-xs mb-1 ${d?'text-zinc-400':'text-zinc-600'}`}>Position</label>
          <select value={position} onChange={e => setPosition(e.target.value)}
            className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`}>
            <option value="bottom">Bottom</option>
            <option value="top">Top</option>
            <option value="center">Center</option>
          </select>
        </div>
      </div>
      <button onClick={handleProcess} disabled={processing} data-testid="subtitles-process-btn"
        className="w-full py-2.5 rounded bg-rose-500 text-white font-semibold hover:bg-rose-600 disabled:opacity-50 flex items-center justify-center gap-2">
        {processing ? <><SpinnerGap className="w-4 h-4 animate-spin" /> Processing...</> : <><Subtitles className="w-4 h-4" /> Burn Subtitles</>}
      </button>
      {result && <a href={`${API.replace('/api','')}${result}`} download className="block w-full py-2.5 rounded bg-emerald-500 text-white font-semibold text-center hover:bg-emerald-600"><DownloadSimple className="w-4 h-4 inline mr-1" />Download Video</a>}
    </div>
  );
};

// ---- Translate Tool ----
const TranslateTool = ({ token, d }) => {
  const [srt, setSrt] = useState(null);
  const [textInput, setTextInput] = useState("");
  const [targetLang, setTargetLang] = useState("km");
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [translated, setTranslated] = useState("");

  const langs = { km: "Khmer", th: "Thai", vi: "Vietnamese", ko: "Korean", ja: "Japanese", en: "English", zh: "Chinese", es: "Spanish", fr: "French", de: "German", pt: "Portuguese", ru: "Russian", ar: "Arabic", id: "Indonesian", hi: "Hindi", ms: "Malay", lo: "Lao", my: "Burmese", it: "Italian", tl: "Filipino" };

  const handleTranslate = async () => {
    if (!srt && !textInput.trim()) return toast.error("Upload SRT or type text");
    setProcessing(true);
    try {
      if (srt) {
        const fd = new FormData();
        fd.append("srt", srt);
        fd.append("target_language", targetLang);
        const r = await axios.post(`${API}/tools/translate-srt`, fd, { headers: { Authorization: `Bearer ${token}` }, timeout: 300000 });
        setResult(r.data.download_url);
        toast.success("SRT translated!");
      } else {
        const r = await axios.post(`${API}/tools/translate-text`, { text: textInput, target_language: targetLang }, { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }, timeout: 60000 });
        setTranslated(r.data.translated);
        toast.success("Text translated!");
      }
    } catch (e) { toast.error(e.response?.data?.detail || "Failed"); }
    finally { setProcessing(false); }
  };

  return (
    <div className="space-y-4">
      <div>
        <label className={`block text-sm font-medium mb-1 ${d?'text-zinc-300':'text-zinc-700'}`}>SRT File (optional)</label>
        <input type="file" accept=".srt" onChange={e => setSrt(e.target.files[0])}
          className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} data-testid="translate-srt-input" />
      </div>
      <div className={`text-center text-xs ${d?'text-zinc-500':'text-zinc-400'}`}>— OR type text —</div>
      <textarea value={textInput} onChange={e => setTextInput(e.target.value)} rows={4} placeholder="Type text to translate..."
        className={`w-full text-sm p-3 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white placeholder:text-zinc-500':'bg-white border-zinc-300 placeholder:text-zinc-400'}`} data-testid="translate-text-input" />
      <div>
        <label className={`block text-xs mb-1 ${d?'text-zinc-400':'text-zinc-600'}`}>Target Language</label>
        <select value={targetLang} onChange={e => setTargetLang(e.target.value)}
          className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} data-testid="translate-lang-select">
          {Object.entries(langs).map(([k,v]) => <option key={k} value={k}>{v}</option>)}
        </select>
      </div>
      <button onClick={handleTranslate} disabled={processing} data-testid="translate-process-btn"
        className="w-full py-2.5 rounded bg-violet-500 text-white font-semibold hover:bg-violet-600 disabled:opacity-50 flex items-center justify-center gap-2">
        {processing ? <><SpinnerGap className="w-4 h-4 animate-spin" /> Translating...</> : <><Translate className="w-4 h-4" /> Translate</>}
      </button>
      {translated && <div className={`p-3 rounded border text-sm ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-gray-50 border-zinc-300'}`} data-testid="translate-result">{translated}</div>}
      {result && <a href={`${API.replace('/api','')}${result}`} download className="block w-full py-2.5 rounded bg-emerald-500 text-white font-semibold text-center hover:bg-emerald-600"><DownloadSimple className="w-4 h-4 inline mr-1" />Download SRT</a>}
    </div>
  );
};

// ---- Trim Tool ----
const TrimTool = ({ token, d }) => {
  const [video, setVideo] = useState(null);
  const [startTime, setStartTime] = useState("00:00:00");
  const [endTime, setEndTime] = useState("00:00:30");
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);

  const handleTrim = async () => {
    if (!video) return toast.error("Upload a video");
    setProcessing(true);
    try {
      const fd = new FormData();
      fd.append("video", video);
      fd.append("start_time", startTime);
      fd.append("end_time", endTime);
      const r = await axios.post(`${API}/tools/trim-video`, fd, { headers: { Authorization: `Bearer ${token}` }, timeout: 600000 });
      setResult(r.data.download_url);
      toast.success("Video trimmed!");
    } catch (e) { toast.error(e.response?.data?.detail || "Failed"); }
    finally { setProcessing(false); }
  };

  return (
    <div className="space-y-4">
      <div>
        <label className={`block text-sm font-medium mb-1 ${d?'text-zinc-300':'text-zinc-700'}`}>Video File</label>
        <input type="file" accept="video/*" onChange={e => setVideo(e.target.files[0])}
          className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} data-testid="trim-video-input" />
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className={`block text-xs mb-1 ${d?'text-zinc-400':'text-zinc-600'}`}>Start Time (HH:MM:SS)</label>
          <input type="text" value={startTime} onChange={e => setStartTime(e.target.value)} placeholder="00:00:00"
            className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} data-testid="trim-start-input" />
        </div>
        <div>
          <label className={`block text-xs mb-1 ${d?'text-zinc-400':'text-zinc-600'}`}>End Time (HH:MM:SS)</label>
          <input type="text" value={endTime} onChange={e => setEndTime(e.target.value)} placeholder="00:00:30"
            className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} data-testid="trim-end-input" />
        </div>
      </div>
      <button onClick={handleTrim} disabled={processing} data-testid="trim-process-btn"
        className="w-full py-2.5 rounded bg-amber-500 text-white font-semibold hover:bg-amber-600 disabled:opacity-50 flex items-center justify-center gap-2">
        {processing ? <><SpinnerGap className="w-4 h-4 animate-spin" /> Trimming...</> : <><Scissors className="w-4 h-4" /> Trim Video</>}
      </button>
      {result && <a href={`${API.replace('/api','')}${result}`} download className="block w-full py-2.5 rounded bg-emerald-500 text-white font-semibold text-center hover:bg-emerald-600"><DownloadSimple className="w-4 h-4 inline mr-1" />Download Trimmed</a>}
    </div>
  );
};

// ---- AI Clips Tool ----
const AIClipsTool = ({ token, d }) => {
  const [video, setVideo] = useState(null);
  const [clipCount, setClipCount] = useState(3);
  const [clipDuration, setClipDuration] = useState(30);
  const [processing, setProcessing] = useState(false);
  const [clips, setClips] = useState([]);

  const handleProcess = async () => {
    if (!video) return toast.error("Upload a video");
    setProcessing(true);
    try {
      const fd = new FormData();
      fd.append("video", video);
      fd.append("clip_count", clipCount);
      fd.append("clip_duration", clipDuration);
      const r = await axios.post(`${API}/tools/ai-clips`, fd, { headers: { Authorization: `Bearer ${token}` }, timeout: 600000 });
      setClips(r.data.clips || []);
      toast.success(`${r.data.clips?.length || 0} clips created!`);
    } catch (e) { toast.error(e.response?.data?.detail || "Failed"); }
    finally { setProcessing(false); }
  };

  return (
    <div className="space-y-4">
      <div>
        <label className={`block text-sm font-medium mb-1 ${d?'text-zinc-300':'text-zinc-700'}`}>Video File</label>
        <input type="file" accept="video/*" onChange={e => setVideo(e.target.files[0])}
          className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} data-testid="aiclips-video-input" />
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className={`block text-xs mb-1 ${d?'text-zinc-400':'text-zinc-600'}`}>Number of Clips</label>
          <input type="number" value={clipCount} onChange={e => setClipCount(e.target.value)} min={1} max={10}
            className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} />
        </div>
        <div>
          <label className={`block text-xs mb-1 ${d?'text-zinc-400':'text-zinc-600'}`}>Clip Duration (sec)</label>
          <input type="number" value={clipDuration} onChange={e => setClipDuration(e.target.value)} min={5} max={120}
            className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} />
        </div>
      </div>
      <button onClick={handleProcess} disabled={processing} data-testid="aiclips-process-btn"
        className="w-full py-2.5 rounded bg-cyan-500 text-white font-semibold hover:bg-cyan-600 disabled:opacity-50 flex items-center justify-center gap-2">
        {processing ? <><SpinnerGap className="w-4 h-4 animate-spin" /> Creating Clips...</> : <><FilmSlate className="w-4 h-4" /> Create AI Clips</>}
      </button>
      {clips.map((c, i) => (
        <a key={i} href={`${API.replace('/api','')}${c.url}`} download
          className={`block p-3 rounded border text-sm ${d?'bg-zinc-800 border-zinc-700 text-white hover:bg-zinc-700':'bg-gray-50 border-zinc-300 hover:bg-gray-100'}`}>
          <DownloadSimple className="w-4 h-4 inline mr-1" />Clip {i+1}: {c.start}s - {c.end}s
        </a>
      ))}
    </div>
  );
};

// ---- TTS Tool ----
const TTSTool = ({ token, d }) => {
  const [text, setText] = useState("");
  const [voice, setVoice] = useState("mms_khmer");
  const [speed, setSpeed] = useState(0);
  const [processing, setProcessing] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);

  const voices = [
    { id: "mms_khmer", name: "Meta AI (Boy) - Khmer" },
    { id: "mms_khmer_f", name: "Meta AI (Girl) - Khmer" },
    { id: "sophea", name: "Sreymom (Girl) - Khmer" },
    { id: "dara", name: "Piseth (Boy) - Khmer" },
    { id: "en_m1", name: "Guy (Boy) - English" },
    { id: "en_f1", name: "Jenny (Girl) - English" },
    { id: "zh_m1", name: "YunXi (Boy) - Chinese" },
    { id: "zh_f1", name: "XiaoXiao (Girl) - Chinese" },
    { id: "th_m1", name: "Niwat (Boy) - Thai" },
    { id: "th_f1", name: "Premwadee (Girl) - Thai" },
  ];

  const handleGenerate = async () => {
    if (!text.trim()) return toast.error("Type some text");
    setProcessing(true);
    try {
      const r = await axios.post(`${API}/tools/text-to-speech`, { text, voice, speed }, {
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        responseType: 'blob', timeout: 60000
      });
      const url = URL.createObjectURL(r.data);
      setAudioUrl(url);
      toast.success("Audio generated!");
    } catch (e) { toast.error("TTS failed"); }
    finally { setProcessing(false); }
  };

  return (
    <div className="space-y-4">
      <textarea value={text} onChange={e => setText(e.target.value)} rows={4} placeholder="Type text here..."
        className={`w-full text-sm p-3 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white placeholder:text-zinc-500':'bg-white border-zinc-300 placeholder:text-zinc-400'}`} data-testid="tts-text-input" />
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className={`block text-xs mb-1 ${d?'text-zinc-400':'text-zinc-600'}`}>Voice</label>
          <select value={voice} onChange={e => setVoice(e.target.value)}
            className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} data-testid="tts-voice-select">
            {voices.map(v => <option key={v.id} value={v.id}>{v.name}</option>)}
          </select>
        </div>
        <div>
          <label className={`block text-xs mb-1 ${d?'text-zinc-400':'text-zinc-600'}`}>Speed: {speed >= 0 ? '+' : ''}{speed}%</label>
          <input type="range" min={-50} max={50} value={speed} onChange={e => setSpeed(Number(e.target.value))}
            className="w-full" />
        </div>
      </div>
      <button onClick={handleGenerate} disabled={processing} data-testid="tts-process-btn"
        className="w-full py-2.5 rounded bg-emerald-500 text-white font-semibold hover:bg-emerald-600 disabled:opacity-50 flex items-center justify-center gap-2">
        {processing ? <><SpinnerGap className="w-4 h-4 animate-spin" /> Generating...</> : <><SpeakerHigh className="w-4 h-4" /> Generate Speech</>}
      </button>
      {audioUrl && (
        <div className="space-y-2">
          <audio controls src={audioUrl} className="w-full" data-testid="tts-audio-player" />
          <a href={audioUrl} download="speech.wav" className="block w-full py-2 rounded bg-emerald-600 text-white font-semibold text-center hover:bg-emerald-700 text-sm">
            <DownloadSimple className="w-4 h-4 inline mr-1" />Download Audio
          </a>
        </div>
      )}
    </div>
  );
};

// ---- Resize Tool ----
const ResizeTool = ({ token, d }) => {
  const [video, setVideo] = useState(null);
  const [preset, setPreset] = useState("1920:1080");
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);

  const presets = [
    { value: "1920:1080", label: "1920x1080 (16:9 Landscape)" },
    { value: "1080:1920", label: "1080x1920 (9:16 Portrait/TikTok)" },
    { value: "1080:1080", label: "1080x1080 (1:1 Square)" },
    { value: "1280:720", label: "1280x720 (HD)" },
    { value: "854:480", label: "854x480 (SD)" },
    { value: "720:1280", label: "720x1280 (9:16 HD Portrait)" },
  ];

  const handleResize = async () => {
    if (!video) return toast.error("Upload a video");
    setProcessing(true);
    try {
      const fd = new FormData();
      fd.append("video", video);
      fd.append("resolution", preset);
      const r = await axios.post(`${API}/tools/resize-video`, fd, { headers: { Authorization: `Bearer ${token}` }, timeout: 600000 });
      setResult(r.data.download_url);
      toast.success("Video resized!");
    } catch (e) { toast.error(e.response?.data?.detail || "Failed"); }
    finally { setProcessing(false); }
  };

  return (
    <div className="space-y-4">
      <div>
        <label className={`block text-sm font-medium mb-1 ${d?'text-zinc-300':'text-zinc-700'}`}>Video File</label>
        <input type="file" accept="video/*" onChange={e => setVideo(e.target.files[0])}
          className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} data-testid="resize-video-input" />
      </div>
      <div>
        <label className={`block text-xs mb-1 ${d?'text-zinc-400':'text-zinc-600'}`}>Size</label>
        <select value={preset} onChange={e => setPreset(e.target.value)}
          className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} data-testid="resize-preset-select">
          {presets.map(p => <option key={p.value} value={p.value}>{p.label}</option>)}
        </select>
      </div>
      <button onClick={handleResize} disabled={processing} data-testid="resize-process-btn"
        className="w-full py-2.5 rounded bg-blue-500 text-white font-semibold hover:bg-blue-600 disabled:opacity-50 flex items-center justify-center gap-2">
        {processing ? <><SpinnerGap className="w-4 h-4 animate-spin" /> Resizing...</> : <><ArrowsOut className="w-4 h-4" /> Resize Video</>}
      </button>
      {result && <a href={`${API.replace('/api','')}${result}`} download className="block w-full py-2.5 rounded bg-emerald-500 text-white font-semibold text-center hover:bg-emerald-600"><DownloadSimple className="w-4 h-4 inline mr-1" />Download Resized</a>}
    </div>
  );
};

// ---- Convert Tool ----
const ConvertTool = ({ token, d }) => {
  const [video, setVideo] = useState(null);
  const [format, setFormat] = useState("mp4");
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);

  const formats = [
    { value: "mp4", label: "MP4" },
    { value: "mov", label: "MOV" },
    { value: "avi", label: "AVI" },
    { value: "webm", label: "WebM" },
    { value: "mkv", label: "MKV" },
    { value: "mp3", label: "MP3 (audio only)" },
    { value: "wav", label: "WAV (audio only)" },
  ];

  const handleConvert = async () => {
    if (!video) return toast.error("Upload a video");
    setProcessing(true);
    try {
      const fd = new FormData();
      fd.append("video", video);
      fd.append("output_format", format);
      const r = await axios.post(`${API}/tools/convert-video`, fd, { headers: { Authorization: `Bearer ${token}` }, timeout: 600000 });
      setResult(r.data.download_url);
      toast.success("Converted!");
    } catch (e) { toast.error(e.response?.data?.detail || "Failed"); }
    finally { setProcessing(false); }
  };

  return (
    <div className="space-y-4">
      <div>
        <label className={`block text-sm font-medium mb-1 ${d?'text-zinc-300':'text-zinc-700'}`}>Video/Audio File</label>
        <input type="file" accept="video/*,audio/*" onChange={e => setVideo(e.target.files[0])}
          className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} data-testid="convert-video-input" />
      </div>
      <div>
        <label className={`block text-xs mb-1 ${d?'text-zinc-400':'text-zinc-600'}`}>Output Format</label>
        <select value={format} onChange={e => setFormat(e.target.value)}
          className={`w-full text-sm p-2 rounded border ${d?'bg-zinc-800 border-zinc-700 text-white':'bg-white border-zinc-300'}`} data-testid="convert-format-select">
          {formats.map(f => <option key={f.value} value={f.value}>{f.label}</option>)}
        </select>
      </div>
      <button onClick={handleConvert} disabled={processing} data-testid="convert-process-btn"
        className="w-full py-2.5 rounded bg-orange-500 text-white font-semibold hover:bg-orange-600 disabled:opacity-50 flex items-center justify-center gap-2">
        {processing ? <><SpinnerGap className="w-4 h-4 animate-spin" /> Converting...</> : <><ArrowsClockwise className="w-4 h-4" /> Convert</>}
      </button>
      {result && <a href={`${API.replace('/api','')}${result}`} download className="block w-full py-2.5 rounded bg-emerald-500 text-white font-semibold text-center hover:bg-emerald-600"><DownloadSimple className="w-4 h-4 inline mr-1" />Download</a>}
    </div>
  );
};

const TOOL_COMPONENTS = {
  "subtitles": SubtitlesTool,
  "translate": TranslateTool,
  "trim": TrimTool,
  "ai-clips": AIClipsTool,
  "tts": TTSTool,
  "resize": ResizeTool,
  "convert": ConvertTool,
};

const ToolsPage = () => {
  const { user, token, isDark, logout } = useAuth();
  const d = isDark;
  const navigate = useNavigate();
  const [activeTool, setActiveTool] = useState(null);

  const ToolComponent = activeTool ? TOOL_COMPONENTS[activeTool] : null;
  const activeToolInfo = TOOLS.find(t => t.id === activeTool);

  return (
    <div className={`min-h-screen ${d?'bg-zinc-950':'bg-gray-50'}`} style={{fontFamily:"'IBM Plex Sans',sans-serif"}}>
      {/* Header */}
      <header className={`sticky top-0 z-50 backdrop-blur-xl shadow-sm ${d?'bg-zinc-950/80 border-b border-zinc-800':'bg-white/70 border-b border-black/10'}`}>
        <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button onClick={() => navigate("/dashboard")} className={`flex items-center gap-2 ${d?'text-zinc-400 hover:text-white':'text-zinc-600 hover:text-zinc-900'}`}>
              <MicrophoneStage className="w-5 h-5" weight="fill" />
              <span className="font-semibold" style={{fontFamily:"'Outfit',sans-serif"}}>VoxiDub</span>
            </button>
            <span className={`text-xs px-2 py-0.5 rounded ${d?'bg-zinc-800 text-zinc-400':'bg-zinc-200 text-zinc-600'}`}>Tools</span>
          </div>
          <div className="flex items-center gap-3">
            <ThemeToggle />
            <button onClick={() => navigate("/dashboard")} className={`text-sm px-3 py-1.5 rounded ${d?'bg-zinc-800 text-zinc-300 hover:bg-zinc-700':'bg-zinc-100 text-zinc-700 hover:bg-zinc-200'}`}>
              <ArrowLeft className="w-3.5 h-3.5 inline mr-1" />Dashboard
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-6 py-8">
        {!activeTool ? (
          <>
            <div className="mb-8">
              <h1 className={`text-2xl font-bold ${d?'text-white':'text-zinc-900'}`}>Video & Audio Tools</h1>
              <p className={`text-sm mt-1 ${d?'text-zinc-400':'text-zinc-500'}`}>Free tools powered by FFmpeg & AI</p>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
              {TOOLS.map((tool, i) => (
                <motion.button key={tool.id}
                  initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
                  onClick={() => setActiveTool(tool.id)}
                  data-testid={`tool-card-${tool.id}`}
                  className={`p-5 rounded-xl border text-left transition-all hover:scale-[1.02] hover:shadow-lg ${d?'bg-zinc-900 border-zinc-800 hover:border-zinc-600':'bg-white border-zinc-200 hover:border-zinc-400'}`}>
                  <div className={`w-10 h-10 rounded-lg ${tool.color} flex items-center justify-center mb-3`}>
                    <tool.icon className="w-5 h-5 text-white" weight="bold" />
                  </div>
                  <div className={`text-sm font-semibold ${d?'text-white':'text-zinc-900'}`}>{tool.name}</div>
                  <div className={`text-xs mt-1 ${d?'text-zinc-500':'text-zinc-500'}`}>{tool.desc}</div>
                </motion.button>
              ))}
            </div>
          </>
        ) : (
          <div>
            <button onClick={() => setActiveTool(null)} className={`flex items-center gap-1.5 text-sm mb-6 ${d?'text-zinc-400 hover:text-white':'text-zinc-600 hover:text-zinc-900'}`} data-testid="tools-back-btn">
              <ArrowLeft className="w-4 h-4" /> Back to Tools
            </button>
            <div className={`max-w-lg mx-auto rounded-xl border p-6 ${d?'bg-zinc-900 border-zinc-800':'bg-white border-zinc-200'}`}>
              <div className="flex items-center gap-3 mb-5">
                <div className={`w-10 h-10 rounded-lg ${activeToolInfo.color} flex items-center justify-center`}>
                  <activeToolInfo.icon className="w-5 h-5 text-white" weight="bold" />
                </div>
                <div>
                  <div className={`text-lg font-semibold ${d?'text-white':'text-zinc-900'}`}>{activeToolInfo.name}</div>
                  <div className={`text-xs ${d?'text-zinc-500':'text-zinc-500'}`}>{activeToolInfo.desc}</div>
                </div>
              </div>
              <ToolComponent token={token} d={d} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ToolsPage;
