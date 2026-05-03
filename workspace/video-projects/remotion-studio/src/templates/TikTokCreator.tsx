import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  OffthreadVideo,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import type {
  BackgroundMusicTrack,
  IconOverlay,
  SoundEffect,
  TikTokCreatorProps,
} from "../types";
import { CaptionRenderer, ProgressBar } from "./heygen-short";

const BGMusic: React.FC<{
  track: BackgroundMusicTrack;
  totalDurationSec: number;
}> = ({ track, totalDurationSec }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const baseVolume = Math.min(track.volume ?? 0.08, 0.15);
  const fadeIn = track.fadeInSec ?? 1;
  const fadeOut = track.fadeOutSec ?? 2;
  const endSec = track.endSec ?? totalDurationSec;
  const trackDur = endSec - track.startSec;
  const currentSec = frame / fps;
  const vol = interpolate(
    currentSec,
    [0, fadeIn, Math.max(fadeIn, trackDur - fadeOut), trackDur],
    [0, baseVolume, baseVolume, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  return (
    <Sequence
      from={Math.round(track.startSec * fps)}
      durationInFrames={Math.round(trackDur * fps)}
    >
      <Audio src={staticFile(track.audioPath)} volume={vol} loop />
    </Sequence>
  );
};

const SFX: React.FC<{ fx: SoundEffect }> = ({ fx }) => {
  const { fps } = useVideoConfig();
  return (
    <Sequence from={Math.round(fx.startSec * fps)} durationInFrames={Math.round((fx.durationSec ?? 3) * fps)}>
      <Audio src={staticFile(fx.audioPath)} volume={fx.volume ?? 0.7} />
    </Sequence>
  );
};

const IconBadge: React.FC<{ overlay: IconOverlay; fps: number }> = ({ overlay, fps }) => {
  const frame = useCurrentFrame();
  const durFrames = Math.round((overlay.endSec - overlay.startSec) * fps);
  const enterFrames = Math.round(0.35 * fps);
  const exitFrames = Math.round(0.3 * fps);
  const size = overlay.size ?? 260;
  const position = overlay.position ?? "top";

  const scale = interpolate(
    frame,
    [0, enterFrames, durFrames - exitFrames, durFrames],
    [0.4, 1, 1, 0.6],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const opacity = interpolate(
    frame,
    [0, enterFrames, durFrames - exitFrames, durFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const bounce = Math.sin((frame / fps) * 4) * 6;

  const posStyle: React.CSSProperties =
    position === "top"
      ? { top: 120, left: 0, right: 0, display: "flex", justifyContent: "center" }
      : position === "top-right"
      ? { top: 120, right: 60 }
      : { top: 120, left: 60 };

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          ...posStyle,
          opacity,
          transform: `translateY(${bounce}px)`,
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 18,
            transform: `scale(${scale})`,
          }}
        >
          <div
            style={{
              width: size,
              height: size,
              borderRadius: size / 2,
              background: overlay.bgColor ?? "#ffffff",
              boxShadow:
                "0 12px 48px rgba(0,0,0,0.6), 0 0 0 8px rgba(255,255,255,0.15)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: size * 0.18,
            }}
          >
            <Img
              src={staticFile(overlay.iconPath)}
              style={{ width: "100%", height: "100%", objectFit: "contain" }}
            />
          </div>
          {overlay.label ? (
            <div
              style={{
                color: overlay.labelColor ?? "#fff",
                fontSize: 64,
                fontWeight: 900,
                fontFamily: "Inter, system-ui, sans-serif",
                textAlign: "center",
                letterSpacing: 1,
                textShadow:
                  "-3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000, 3px 3px 0 #000, 0 0 24px rgba(0,0,0,0.9)",
              }}
            >
              {overlay.label}
            </div>
          ) : null}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const IconOverlayLayer: React.FC<{ overlay: IconOverlay }> = ({ overlay }) => {
  const { fps } = useVideoConfig();
  const fromFrame = Math.round(overlay.startSec * fps);
  const durFrames = Math.round((overlay.endSec - overlay.startSec) * fps);
  return (
    <Sequence from={fromFrame} durationInFrames={durFrames}>
      <IconBadge overlay={overlay} fps={fps} />
    </Sequence>
  );
};

export const TikTokCreator: React.FC<TikTokCreatorProps> = ({
  videoPath,
  videoStartSec = 0,
  durationSeconds,
  captions,
  iconOverlays,
  soundEffects,
  backgroundMusic,
  hookBoostSec = 5,
  showProgressBar = true,
  footerText,
  volume = 1,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const currentSec = frame / fps;

  const hookScale = interpolate(
    currentSec,
    [0, hookBoostSec * 0.5, hookBoostSec],
    [1.15, 1.08, 1.0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const kenBurns = 1 + ((currentSec / durationSeconds) * 0.04);
  const scale = hookScale * kenBurns;

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {/* Video with hook zoom + subtle ken burns */}
      <AbsoluteFill style={{ transform: `scale(${scale})`, transformOrigin: "center center" }}>
        <OffthreadVideo
          src={staticFile(videoPath)}
          startFrom={Math.round(videoStartSec * fps)}
          volume={volume}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      </AbsoluteFill>

      {/* Dark vignette for caption contrast */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.4) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* Icon overlays for each MCP */}
      {iconOverlays?.map((o, i) => (
        <IconOverlayLayer key={i} overlay={o} />
      ))}

      {/* Captions */}
      <CaptionRenderer
        captions={captions}
        globalStartSec={0}
        totalDuration={durationSeconds}
        defaultCaptionPosition={62}
      />

      {/* BGM */}
      {backgroundMusic?.map((t, i) => (
        <BGMusic key={i} track={t} totalDurationSec={durationSeconds} />
      ))}

      {/* SFX */}
      {soundEffects?.map((fx, i) => (
        <SFX key={i} fx={fx} />
      ))}

      {/* Footer */}
      {footerText ? (
        <div
          style={{
            position: "absolute",
            bottom: 40,
            left: 0,
            right: 0,
            textAlign: "center",
            color: "rgba(255,255,255,0.85)",
            fontSize: 32,
            fontWeight: 700,
            fontFamily: "Inter, system-ui, sans-serif",
            textShadow: "0 2px 12px rgba(0,0,0,0.8)",
            letterSpacing: 0.5,
          }}
        >
          {footerText}
        </div>
      ) : null}

      {/* Progress bar */}
      {showProgressBar && <ProgressBar totalDurationSec={durationSeconds} />}
    </AbsoluteFill>
  );
};
