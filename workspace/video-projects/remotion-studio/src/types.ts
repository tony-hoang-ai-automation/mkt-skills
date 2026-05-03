export type DarkMinimalProps = {
  title: string;
  items: string[];
  watermark: string;
  bgVideo: string;
  bgMusic?: string;
  durationSeconds?: number;
};

export type BoldHighlightProps = {
  title: string;
  bodyLines: Array<{
    text: string;
    highlights?: string[];
  }>;
  quote?: string;
  accentColor?: string;
  watermark: string;
  bgVideo: string;
  bgMusic?: string;
  durationSeconds?: number;
};

export type EpicFullscreenProps = {
  lines: Array<{
    text: string;
    isHighlight?: boolean;
  }>;
  accentColor?: string;
  bgVideo: string;
  bgMusic?: string;
  durationSeconds?: number;
};

export type ImageKenBurnsProps = {
  imagePath: string;
  bgColor?: string;
  bgMusic?: string;
  durationSeconds?: number;
};

export type TextSection = {
  lines: string[];
  startSec: number;
  durationSec: number;
  fontSize?: number;
  fontWeight?: number;
  color?: string;
  lineHeight?: number;
};

export type WordTiming = {
  word: string;
  start: number; // seconds (from Whisper word_timestamps)
  end: number;
};

export type CaptionSegment = {
  text: string;
  startSec: number;
  endSec: number;
  words?: WordTiming[]; // word-level timestamps for precise sync
  highlights?: string[];
  highlightColor?: string;
  emoji?: string; // AnimatedEmoji name (e.g. "mind-blown") or Unicode fallback
  style?: "normal" | "hook" | "pain" | "solution" | "cta";
  textEffect?: "none" | "word-by-word" | "deep-glow" | "flicker" | "typewriter" | "slam" | "wave";
  captionPosition?: number; // top % position (default 55, near neck area)
};

export type BRollOverlay = {
  mediaPath: string; // image or video path in public/media/
  startSec: number;
  endSec: number;
  position?: "center" | "top-right" | "bottom-left";
  scale?: number; // default 0.6
  borderRadius?: number; // default 20
  label?: string;
};

/** Legacy type — use VideoClip instead */
export type HeyGenClip = {
  videoPath: string;
  durationSeconds: number;
  /** Absolute timeline start in seconds. If set, clip is positioned absolutely (overlapping allowed). If undefined, falls back to sequential stacking. */
  startSec?: number;
  /** Source offset — skip first N seconds of the source video. */
  startFromSec?: number;
  /** Override the global muted behavior. If undefined, uses `!!audioPath`. */
  muted?: boolean;
  /** Stacking order — higher values render on top. Default 0. B-roll visuals should use zIndex >= 10 to sit above avatar clips. */
  zIndex?: number;
};

/**
 * Unified clip that can appear in the timeline.
 * - "avatar": HeyGen avatar video (lip-synced to voiceover)
 * - "broll": Full-screen b-roll visual (video/image), audio muted
 * - "media": Generic video/image clip with optional audio
 */
export type VideoClip =
  | AvatarClip
  | BRollClip
  | MediaClip;

export type AvatarClip = {
  type: "avatar";
  videoPath: string;
  durationSeconds: number;
};

export type BRollClip = {
  type: "broll";
  mediaPath: string;        // video or image in public/media/
  durationSeconds: number;
  overlayText?: string;      // text overlay (e.g. "#1 TASTE")
  position?: "fullscreen" | "center" | "top-right" | "bottom-left" | "bottom";
  borderRadius?: number;
};

export type MediaClip = {
  type: "media";
  mediaPath: string;
  durationSeconds: number;
  volume?: number;           // 0-1, default 0
};

export type SoundEffect = {
  audioPath: string;
  startSec: number;
  volume?: number;
  startFromSec?: number; // skip N seconds at the beginning of the audio file
  durationSec?: number;  // stop playing after N seconds
};

export type ZoomPulse = {
  timeSec: number;
  scale?: number; // peak scale, default 1.15
  durationFrames?: number; // total pulse duration in frames, default 9 (~0.3s)
  type?: "punch" | "hold" | "slow"; // punch=quick in/out, hold=zoom in + hold + ease out, slow=gradual in/out
  holdSec?: number; // seconds to hold at peak scale (only for "hold" type, default 3)
};

export type BackgroundMusicTrack = {
  audioPath: string;
  startSec: number; // when this track starts playing
  endSec?: number; // when to stop (defaults to end of video)
  volume?: number; // 0.0–1.0 (default 0.12 — subtle background)
  fadeInSec?: number; // fade-in duration (default 1)
  fadeOutSec?: number; // fade-out duration (default 2)
};

export type SceneTransitionConfig = {
  type?: "flash" | "fade-black" | "glitch" | "swipe-left" | "swipe-right" | "zoom-blur";
  durationFrames?: number; // default 12 (~0.4s)
};

export type HeyGenShortProps = {
  clips: HeyGenClip[];
  captions: CaptionSegment[];
  durationSeconds: number;
  crossFadeFrames?: number;
  showProgressBar?: boolean;
  soundEffects?: SoundEffect[];
  zoomPulses?: ZoomPulse[];
  bRollOverlays?: BRollOverlay[];
  backgroundMusic?: BackgroundMusicTrack[]; // multiple tracks with per-track volume & timing
  hookBoostSec?: number; // auto-boost zoom in first N seconds (default 0 = disabled)
  defaultCaptionPosition?: number; // global caption top% (default 55)
  audioPath?: string; // full audio track — plays instead of clip audio (mutes all clips)
  footerText?: string; // centered footer text (e.g. "@tranvanhoang.com")
  outro?: OutroCard; // end card with thank you + CTA
  sceneTransition?: SceneTransitionConfig; // transition effect between clips (default "flash")
};

export type OutroCard = {
  durationSeconds: number; // how long to show (e.g. 3)
  title: string; // main text (e.g. "Cảm ơn bạn đã xem!")
  subtitle?: string; // CTA text (e.g. "Vào tranvanhoang.com/qua để nhận template AI")
  bgColor?: string; // background color (default "#000")
  profileImage?: string; // profile photo path in public/ (e.g. "hoang profile.webp")
};

export type PromptTypingProps = {
  text: string;
  durationSeconds: number;
  title?: string; // label above input box (default "Prompt")
  startDelaySec?: number; // delay before typing starts (default 0.5)
  endPauseSec?: number; // pause after typing finishes (default 1.0)
};

export type ProgressiveReductionProps = {
  sections: TextSection[];
  watermark: string;
  bgVideo: string;
  bgMusic?: string;
  durationSeconds: number;
};

export type IconOverlay = {
  iconPath: string;
  startSec: number;
  endSec: number;
  label?: string;
  labelColor?: string;
  bgColor?: string;
  position?: "top" | "top-right" | "top-left";
  size?: number;
};

export type NewsScene =
  | {
      type: "hero";
      startSec: number;
      durationSec: number;
      headline: string;
      subheadline?: string;
      dateChip?: string;
      logo?: "vercel" | "nextjs" | "google";
      emphasisWord?: string;
    }
  | {
      type: "stat";
      startSec: number;
      durationSec: number;
      value: string;
      label: string;
      subLabel?: string;
      color?: "red" | "yellow" | "cyan" | "green";
    }
  | {
      type: "question";
      startSec: number;
      durationSec: number;
      question: string;
      kicker?: string;
    }
  | {
      type: "attackChain";
      startSec: number;
      durationSec: number;
      title: string;
      nodes: Array<{
        label: string;
        sub?: string;
        icon: "hacker" | "context" | "oauth" | "google" | "vercel" | "shield";
        highlight?: boolean;
      }>;
    }
  | {
      type: "leakList";
      startSec: number;
      durationSec: number;
      title: string;
      subtitle?: string;
      items: string[];
    }
  | {
      type: "quote";
      startSec: number;
      durationSec: number;
      text: string;
      author: string;
      role?: string;
      accent?: "red" | "cyan" | "yellow";
    }
  | {
      type: "marketListing";
      startSec: number;
      durationSec: number;
      source: string;
      actor: string;
      price: string;
      disclaimer?: string;
    }
  | {
      type: "steps";
      startSec: number;
      durationSec: number;
      title: string;
      steps: Array<{ label: string; detail?: string }>;
    }
  | {
      type: "cta";
      startSec: number;
      durationSec: number;
      prompt: string;
      brand: string;
      tagline: string;
    };

export type NewsCaptionWord = { word: string; start: number; end: number };

export type NewsCaption = {
  text: string;
  startSec: number;
  endSec: number;
  words?: NewsCaptionWord[];
  highlights?: string[];
};

export type NewsShareProps = {
  audioPath: string;
  durationSeconds: number;
  breakingLabel?: string;
  dateLabel?: string;
  brandName?: string;
  brandTagline?: string;
  tickerItems: string[];
  scenes: NewsScene[];
  captions: NewsCaption[];
  bgMusicPath?: string;
  bgMusicVolume?: number;
};

export type TikTokCreatorProps = {
  videoPath: string;
  videoStartSec?: number;
  durationSeconds: number;
  captions: CaptionSegment[];
  iconOverlays?: IconOverlay[];
  soundEffects?: SoundEffect[];
  backgroundMusic?: BackgroundMusicTrack[];
  hookBoostSec?: number;
  showProgressBar?: boolean;
  footerText?: string;
  volume?: number;
};
