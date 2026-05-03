import React from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";
import type { NewsShareProps, NewsScene, NewsCaption } from "../types";
import { loadFonts, fontFamily } from "../fonts";
import {
  VercelLogo,
  NextLogo,
  GoogleLogo,
  HackerIcon,
  ShieldIcon,
  OAuthIcon,
  ContextIcon,
  KeyIcon,
  WarningIcon,
  LiveDotIcon,
  IconByName,
} from "./news-share/Icons";

loadFonts();

const COLORS = {
  bg: "#05070F",
  bgGradEnd: "#0A1230",
  red: "#EF4444",
  redDeep: "#B91C1C",
  yellow: "#FDE047",
  cyan: "#22D3EE",
  green: "#22C55E",
  white: "#F8FAFC",
  dim: "#64748B",
  panel: "rgba(255,255,255,0.04)",
  panelBorder: "rgba(148,163,184,0.18)",
};

/* ─────────────────── Background — animated grid + scanline ─────────────────── */
const TechBackground: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const scanY = ((frame * 4) % 2100) - 100;
  const pulseAlpha =
    0.35 + Math.sin((frame / fps) * 2) * 0.1;

  return (
    <AbsoluteFill>
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse at 50% 30%, ${COLORS.bgGradEnd} 0%, ${COLORS.bg} 60%, #000 100%)`,
        }}
      />
      {/* grid */}
      <AbsoluteFill
        style={{
          backgroundImage: `
            linear-gradient(rgba(59,130,246,0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(59,130,246,0.08) 1px, transparent 1px)
          `,
          backgroundSize: "80px 80px",
          opacity: pulseAlpha,
        }}
      />
      {/* accent glow */}
      <div
        style={{
          position: "absolute",
          top: -200,
          right: -200,
          width: 700,
          height: 700,
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(239,68,68,0.3), transparent 70%)",
          filter: "blur(40px)",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: -200,
          left: -200,
          width: 700,
          height: 700,
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(34,211,238,0.22), transparent 70%)",
          filter: "blur(60px)",
        }}
      />
      {/* scan line */}
      <div
        style={{
          position: "absolute",
          top: scanY,
          left: 0,
          right: 0,
          height: 140,
          background:
            "linear-gradient(to bottom, transparent, rgba(34,211,238,0.12), transparent)",
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};

/* ─────────────────── Breaking Banner (top) ─────────────────── */
const BreakingBanner: React.FC<{
  breakingLabel: string;
  dateLabel: string;
}> = ({ breakingLabel, dateLabel }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pulse = 0.55 + Math.sin((frame / fps) * 6) * 0.45;

  return (
    <div
      style={{
        position: "absolute",
        top: 48,
        left: 32,
        right: 32,
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        zIndex: 20,
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 14,
          background: `linear-gradient(90deg, ${COLORS.red}, ${COLORS.redDeep})`,
          padding: "14px 24px",
          borderRadius: 10,
          boxShadow: `0 8px 24px rgba(239,68,68,0.35), 0 0 ${pulse * 30}px rgba(239,68,68,0.6)`,
        }}
      >
        <div
          style={{
            width: 14,
            height: 14,
            borderRadius: "50%",
            background: "#fff",
            opacity: pulse,
            boxShadow: `0 0 12px rgba(255,255,255,${pulse})`,
          }}
        />
        <div
          style={{
            fontFamily,
            color: "#fff",
            fontWeight: 900,
            fontSize: 26,
            letterSpacing: 2,
          }}
        >
          {breakingLabel}
        </div>
      </div>

      <div
        style={{
          fontFamily,
          color: COLORS.white,
          fontWeight: 700,
          fontSize: 22,
          letterSpacing: 1.5,
          background: COLORS.panel,
          border: `1px solid ${COLORS.panelBorder}`,
          borderRadius: 8,
          padding: "12px 18px",
          backdropFilter: "blur(6px)",
        }}
      >
        {dateLabel}
      </div>
    </div>
  );
};

/* ─────────────────── Ticker (bottom scrolling) ─────────────────── */
const Ticker: React.FC<{ items: string[]; brand: string }> = ({
  items,
  brand,
}) => {
  const frame = useCurrentFrame();
  const tickerText = items.join("   •   ");
  const scrollX = (frame * 2.2) % 2400;

  return (
    <div
      style={{
        position: "absolute",
        bottom: 110,
        left: 0,
        right: 0,
        height: 58,
        display: "flex",
        alignItems: "center",
        background: "linear-gradient(90deg, #000, #0a0e27 50%, #000)",
        borderTop: `2px solid ${COLORS.red}`,
        borderBottom: `1px solid ${COLORS.panelBorder}`,
        zIndex: 19,
      }}
    >
      <div
        style={{
          background: COLORS.red,
          padding: "12px 20px",
          fontFamily,
          color: "#fff",
          fontWeight: 900,
          fontSize: 22,
          letterSpacing: 1.5,
          height: "100%",
          display: "flex",
          alignItems: "center",
          zIndex: 2,
          boxShadow: "4px 0 16px rgba(0,0,0,0.6)",
        }}
      >
        {brand}
      </div>
      <div
        style={{
          flex: 1,
          overflow: "hidden",
          position: "relative",
          height: "100%",
        }}
      >
        <div
          style={{
            position: "absolute",
            whiteSpace: "nowrap",
            transform: `translateX(-${scrollX}px)`,
            fontFamily,
            color: COLORS.white,
            fontWeight: 600,
            fontSize: 22,
            letterSpacing: 0.5,
            lineHeight: "58px",
          }}
        >
          {`${tickerText}   •   ${tickerText}   •   ${tickerText}`}
        </div>
      </div>
    </div>
  );
};

/* ─────────────────── Progress bar (very bottom) ─────────────────── */
const ProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const progress = frame / durationInFrames;
  return (
    <div
      style={{
        position: "absolute",
        bottom: 0,
        left: 0,
        right: 0,
        height: 8,
        background: "rgba(255,255,255,0.08)",
        zIndex: 21,
      }}
    >
      <div
        style={{
          width: `${progress * 100}%`,
          height: "100%",
          background: `linear-gradient(90deg, ${COLORS.red}, ${COLORS.yellow})`,
          boxShadow: `0 0 12px ${COLORS.yellow}`,
        }}
      />
    </div>
  );
};

/* ─────────────────── Live logo badge (top-left ident) ─────────────────── */
const BrandIdent: React.FC<{ brand: string; tagline: string }> = ({
  brand,
  tagline,
}) => (
  <div
    style={{
      position: "absolute",
      top: 130,
      left: 32,
      display: "flex",
      alignItems: "center",
      gap: 10,
      zIndex: 18,
      padding: "8px 14px",
      background: "rgba(5,7,15,0.7)",
      border: `1px solid ${COLORS.panelBorder}`,
      borderRadius: 8,
      backdropFilter: "blur(6px)",
    }}
  >
    <LiveDotIcon size={10} color={COLORS.red} />
    <div
      style={{
        fontFamily,
        color: COLORS.white,
        fontWeight: 800,
        fontSize: 16,
        letterSpacing: 1,
      }}
    >
      {brand}
    </div>
    <div
      style={{
        fontFamily,
        color: COLORS.dim,
        fontWeight: 500,
        fontSize: 13,
        letterSpacing: 0.5,
      }}
    >
      {tagline}
    </div>
  </div>
);

/* ─────────────────── Word-by-word caption ─────────────────── */
const CurrentCaption: React.FC<{ captions: NewsCaption[] }> = ({ captions }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sec = frame / fps;

  const active = captions.find((c) => sec >= c.startSec && sec < c.endSec);
  if (!active) return null;

  const highlightSet = new Set(
    (active.highlights ?? []).map((h) => h.toLowerCase())
  );

  // Fade in/out
  const local = sec - active.startSec;
  const total = active.endSec - active.startSec;
  const opacity = interpolate(
    local,
    [0, 0.2, Math.max(0.2, total - 0.2), total],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <div
      style={{
        position: "absolute",
        left: 56,
        right: 56,
        bottom: 195,
        zIndex: 17,
        opacity,
      }}
    >
      <div
        style={{
          background:
            "linear-gradient(180deg, rgba(5,7,15,0.78), rgba(10,14,39,0.92))",
          border: `1px solid ${COLORS.panelBorder}`,
          borderLeft: `4px solid ${COLORS.yellow}`,
          borderRadius: 14,
          padding: "22px 28px",
          backdropFilter: "blur(10px)",
          boxShadow: "0 18px 60px rgba(0,0,0,0.5)",
        }}
      >
        <div
          style={{
            fontFamily,
            color: COLORS.white,
            fontWeight: 700,
            fontSize: 38,
            lineHeight: 1.3,
            letterSpacing: 0.2,
            display: "flex",
            flexWrap: "wrap",
            gap: "0.28em",
          }}
        >
          {active.words && active.words.length > 0
            ? active.words.map((w, i) => {
                const isCurrent = sec >= w.start && sec < w.end;
                const hasPassed = sec >= w.end;
                const isHighlight = highlightSet.has(
                  w.word.replace(/[.,!?:;]/g, "").toLowerCase()
                );
                const color = isCurrent
                  ? COLORS.yellow
                  : isHighlight
                    ? COLORS.cyan
                    : hasPassed
                      ? COLORS.white
                      : "rgba(248,250,252,0.55)";
                return (
                  <span
                    key={i}
                    style={{
                      color,
                      fontWeight: isCurrent || isHighlight ? 900 : 700,
                      textShadow: isCurrent
                        ? `0 0 16px ${COLORS.yellow}`
                        : "none",
                      transform: isCurrent ? "scale(1.06)" : "scale(1)",
                      display: "inline-block",
                      transition: "color 80ms linear",
                    }}
                  >
                    {w.word}
                  </span>
                );
              })
            : active.text}
        </div>
      </div>
    </div>
  );
};

/* ─────────────────── Scene helpers ─────────────────── */
const sceneFade = (localFrame: number, fps: number, durFrames: number) => {
  const fadeIn = Math.min(0.35 * fps, durFrames * 0.25);
  const fadeOut = Math.min(0.35 * fps, durFrames * 0.25);
  return interpolate(
    localFrame,
    [0, fadeIn, Math.max(fadeIn, durFrames - fadeOut), durFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
};

const SceneFrame: React.FC<{
  children: React.ReactNode;
  opacity: number;
}> = ({ children, opacity }) => (
  <div
    style={{
      position: "absolute",
      top: 210,
      left: 56,
      right: 56,
      bottom: 290,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      opacity,
    }}
  >
    {children}
  </div>
);

/* ─────────────────── HERO scene ─────────────────── */
const HeroScene: React.FC<{
  scene: Extract<NewsScene, { type: "hero" }>;
}> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const durF = Math.round(scene.durationSec * fps);
  const op = sceneFade(frame, fps, durF);

  const titleY = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 90 },
    durationInFrames: 18,
  });
  const glitchOn = scene.emphasisWord && (frame % 18 < 3 || frame % 18 === 8);

  return (
    <SceneFrame opacity={op}>
      <div style={{ width: "100%", textAlign: "center" }}>
        {scene.logo && (
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              marginBottom: 40,
              transform: `scale(${0.6 + titleY * 0.4})`,
              opacity: titleY,
            }}
          >
            <IconByName name={scene.logo} size={160} />
          </div>
        )}
        {scene.dateChip && (
          <div
            style={{
              display: "inline-block",
              background: "rgba(239,68,68,0.16)",
              border: `1px solid ${COLORS.red}`,
              color: COLORS.red,
              padding: "8px 18px",
              borderRadius: 8,
              fontFamily,
              fontWeight: 800,
              fontSize: 22,
              letterSpacing: 2,
              marginBottom: 30,
            }}
          >
            {scene.dateChip}
          </div>
        )}
        <div
          style={{
            fontFamily,
            color: COLORS.white,
            fontWeight: 900,
            fontSize: 120,
            lineHeight: 1.05,
            letterSpacing: -1,
            transform: `translateY(${(1 - titleY) * 40}px)`,
            textShadow: "0 10px 40px rgba(0,0,0,0.8)",
          }}
        >
          {scene.headline.split(" ").map((w, i) => {
            const isEmph =
              scene.emphasisWord &&
              w.toLowerCase().includes(scene.emphasisWord.toLowerCase());
            return (
              <span
                key={i}
                style={{
                  color: isEmph ? COLORS.red : COLORS.white,
                  textShadow: isEmph
                    ? `0 0 30px ${COLORS.red}, 0 0 60px ${COLORS.red}`
                    : "none",
                  display: "inline-block",
                  transform: isEmph && glitchOn ? "skewX(-4deg)" : "none",
                  marginRight: 20,
                }}
              >
                {w}
              </span>
            );
          })}
        </div>
        {scene.subheadline && (
          <div
            style={{
              marginTop: 30,
              fontFamily,
              color: COLORS.dim,
              fontWeight: 500,
              fontSize: 36,
              lineHeight: 1.3,
              opacity: titleY,
            }}
          >
            {scene.subheadline}
          </div>
        )}
      </div>
    </SceneFrame>
  );
};

/* ─────────────────── STAT scene ─────────────────── */
const StatScene: React.FC<{
  scene: Extract<NewsScene, { type: "stat" }>;
}> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const durF = Math.round(scene.durationSec * fps);
  const op = sceneFade(frame, fps, durF);
  const color =
    scene.color === "red"
      ? COLORS.red
      : scene.color === "cyan"
        ? COLORS.cyan
        : scene.color === "green"
          ? COLORS.green
          : COLORS.yellow;

  const pop = spring({
    frame,
    fps,
    config: { damping: 8, stiffness: 140, mass: 0.6 },
    durationInFrames: 24,
  });

  return (
    <SceneFrame opacity={op}>
      <div style={{ width: "100%", textAlign: "center" }}>
        <div
          style={{
            fontFamily,
            color: COLORS.dim,
            fontSize: 34,
            fontWeight: 700,
            letterSpacing: 4,
            textTransform: "uppercase",
            marginBottom: 30,
            opacity: pop,
          }}
        >
          {scene.label}
        </div>
        <div
          style={{
            fontFamily,
            color,
            fontSize: 280,
            fontWeight: 900,
            lineHeight: 1,
            letterSpacing: -6,
            transform: `scale(${0.4 + pop * 0.6})`,
            textShadow: `0 0 60px ${color}, 0 0 120px ${color}80`,
          }}
        >
          {scene.value}
        </div>
        {scene.subLabel && (
          <div
            style={{
              marginTop: 30,
              fontFamily,
              color: COLORS.white,
              fontSize: 34,
              fontWeight: 700,
              opacity: pop,
            }}
          >
            {scene.subLabel}
          </div>
        )}
      </div>
    </SceneFrame>
  );
};

/* ─────────────────── QUESTION scene ─────────────────── */
const QuestionScene: React.FC<{
  scene: Extract<NewsScene, { type: "question" }>;
}> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const durF = Math.round(scene.durationSec * fps);
  const op = sceneFade(frame, fps, durF);
  const glow = 0.6 + Math.sin((frame / fps) * 4) * 0.4;

  return (
    <SceneFrame opacity={op}>
      <div style={{ width: "100%", textAlign: "center" }}>
        {scene.kicker && (
          <div
            style={{
              fontFamily,
              color: COLORS.red,
              fontSize: 30,
              fontWeight: 800,
              letterSpacing: 4,
              textTransform: "uppercase",
              marginBottom: 30,
            }}
          >
            {scene.kicker}
          </div>
        )}
        <div
          style={{
            fontFamily,
            color: COLORS.white,
            fontSize: 88,
            fontWeight: 900,
            lineHeight: 1.1,
            letterSpacing: -1,
            textShadow: `0 0 ${glow * 40}px ${COLORS.cyan}`,
          }}
        >
          {scene.question}
        </div>
        <div
          style={{
            marginTop: 40,
            fontFamily,
            color: COLORS.cyan,
            fontSize: 120,
            fontWeight: 900,
            opacity: glow,
          }}
        >
          ?
        </div>
      </div>
    </SceneFrame>
  );
};

/* ─────────────────── ATTACK CHAIN scene ─────────────────── */
const AttackChainScene: React.FC<{
  scene: Extract<NewsScene, { type: "attackChain" }>;
}> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const durF = Math.round(scene.durationSec * fps);
  const op = sceneFade(frame, fps, durF);

  // Reveal nodes one by one
  const perNode = durF / (scene.nodes.length + 1);

  return (
    <SceneFrame opacity={op}>
      <div style={{ width: "100%" }}>
        <div
          style={{
            fontFamily,
            color: COLORS.red,
            fontSize: 30,
            fontWeight: 800,
            letterSpacing: 4,
            textTransform: "uppercase",
            textAlign: "center",
            marginBottom: 40,
          }}
        >
          {scene.title}
        </div>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 18,
          }}
        >
          {scene.nodes.map((node, i) => {
            const startFrame = Math.round(perNode * i);
            const reveal = spring({
              frame: Math.max(0, frame - startFrame),
              fps,
              config: { damping: 16, stiffness: 120 },
              durationInFrames: 14,
            });
            const arrowStartFrame = Math.round(perNode * (i + 0.7));
            const arrowReveal =
              i < scene.nodes.length - 1
                ? interpolate(frame, [arrowStartFrame, arrowStartFrame + 8], [0, 1], {
                    extrapolateLeft: "clamp",
                    extrapolateRight: "clamp",
                  })
                : 0;
            return (
              <React.Fragment key={i}>
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 26,
                    background: node.highlight
                      ? "linear-gradient(90deg, rgba(239,68,68,0.25), rgba(239,68,68,0.05))"
                      : "rgba(255,255,255,0.04)",
                    border: node.highlight
                      ? `2px solid ${COLORS.red}`
                      : `1px solid ${COLORS.panelBorder}`,
                    borderRadius: 16,
                    padding: "22px 28px",
                    transform: `translateX(${(1 - reveal) * -80}px)`,
                    opacity: reveal,
                    boxShadow: node.highlight
                      ? `0 0 32px rgba(239,68,68,0.4)`
                      : "0 6px 20px rgba(0,0,0,0.4)",
                  }}
                >
                  <div
                    style={{
                      width: 88,
                      height: 88,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      borderRadius: 12,
                      background: "rgba(5,7,15,0.6)",
                      border: `1px solid ${COLORS.panelBorder}`,
                      flexShrink: 0,
                    }}
                  >
                    <IconByName name={node.icon} size={56} />
                  </div>
                  <div style={{ flex: 1 }}>
                    <div
                      style={{
                        fontFamily,
                        color: node.highlight ? COLORS.red : COLORS.white,
                        fontWeight: 900,
                        fontSize: 40,
                        letterSpacing: -0.5,
                        lineHeight: 1.1,
                      }}
                    >
                      {node.label}
                    </div>
                    {node.sub && (
                      <div
                        style={{
                          fontFamily,
                          color: COLORS.dim,
                          fontSize: 22,
                          fontWeight: 500,
                          marginTop: 4,
                        }}
                      >
                        {node.sub}
                      </div>
                    )}
                  </div>
                </div>
                {i < scene.nodes.length - 1 && (
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "center",
                      height: 34,
                      alignItems: "center",
                    }}
                  >
                    <div
                      style={{
                        width: 4,
                        height: `${arrowReveal * 30}px`,
                        background: `linear-gradient(180deg, ${COLORS.red}, ${COLORS.yellow})`,
                        borderRadius: 2,
                        boxShadow: `0 0 10px ${COLORS.red}`,
                      }}
                    />
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </SceneFrame>
  );
};

/* ─────────────────── LEAK LIST scene ─────────────────── */
const LeakListScene: React.FC<{
  scene: Extract<NewsScene, { type: "leakList" }>;
}> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const durF = Math.round(scene.durationSec * fps);
  const op = sceneFade(frame, fps, durF);
  const perItem = durF / (scene.items.length + 1);

  return (
    <SceneFrame opacity={op}>
      <div style={{ width: "100%" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 14,
            justifyContent: "center",
            marginBottom: 20,
          }}
        >
          <WarningIcon size={44} />
          <div
            style={{
              fontFamily,
              color: COLORS.red,
              fontWeight: 900,
              fontSize: 44,
              letterSpacing: 2,
              textTransform: "uppercase",
            }}
          >
            {scene.title}
          </div>
        </div>
        {scene.subtitle && (
          <div
            style={{
              fontFamily,
              color: COLORS.dim,
              fontSize: 26,
              fontWeight: 500,
              textAlign: "center",
              marginBottom: 40,
            }}
          >
            {scene.subtitle}
          </div>
        )}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: scene.items.length > 4 ? "1fr 1fr" : "1fr",
            gap: 14,
          }}
        >
          {scene.items.map((item, i) => {
            const startFrame = Math.round(perItem * i);
            const reveal = spring({
              frame: Math.max(0, frame - startFrame),
              fps,
              config: { damping: 14, stiffness: 120 },
              durationInFrames: 14,
            });
            return (
              <div
                key={i}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 16,
                  background: "rgba(239,68,68,0.1)",
                  border: `1px solid ${COLORS.red}`,
                  borderRadius: 12,
                  padding: "18px 22px",
                  opacity: reveal,
                  transform: `scale(${0.9 + reveal * 0.1})`,
                }}
              >
                <KeyIcon size={40} color={COLORS.yellow} />
                <div
                  style={{
                    fontFamily,
                    color: COLORS.white,
                    fontWeight: 800,
                    fontSize: 34,
                    letterSpacing: -0.3,
                  }}
                >
                  {item}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </SceneFrame>
  );
};

/* ─────────────────── QUOTE scene ─────────────────── */
const QuoteScene: React.FC<{
  scene: Extract<NewsScene, { type: "quote" }>;
}> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const durF = Math.round(scene.durationSec * fps);
  const op = sceneFade(frame, fps, durF);
  const accent =
    scene.accent === "red"
      ? COLORS.red
      : scene.accent === "yellow"
        ? COLORS.yellow
        : COLORS.cyan;

  const authorFade = interpolate(
    frame,
    [Math.round(fps * 0.5), Math.round(fps * 0.9)],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <SceneFrame opacity={op}>
      <div style={{ width: "100%" }}>
        <div
          style={{
            fontFamily,
            color: accent,
            fontSize: 180,
            fontWeight: 900,
            lineHeight: 0.5,
            marginBottom: 20,
            marginLeft: -10,
          }}
        >
          “
        </div>
        <div
          style={{
            fontFamily,
            color: COLORS.white,
            fontWeight: 700,
            fontSize: 58,
            lineHeight: 1.25,
            letterSpacing: -0.3,
            fontStyle: "italic",
            borderLeft: `6px solid ${accent}`,
            paddingLeft: 28,
          }}
        >
          {scene.text}
        </div>
        <div
          style={{
            marginTop: 36,
            paddingLeft: 34,
            opacity: authorFade,
            transform: `translateY(${(1 - authorFade) * 16}px)`,
          }}
        >
          <div
            style={{
              fontFamily,
              color: accent,
              fontWeight: 900,
              fontSize: 36,
            }}
          >
            — {scene.author}
          </div>
          {scene.role && (
            <div
              style={{
                fontFamily,
                color: COLORS.dim,
                fontSize: 24,
                fontWeight: 500,
                marginTop: 6,
              }}
            >
              {scene.role}
            </div>
          )}
        </div>
      </div>
    </SceneFrame>
  );
};

/* ─────────────────── MARKET LISTING scene (Shiny Hunters / $2M) ─────────────────── */
const MarketListingScene: React.FC<{
  scene: Extract<NewsScene, { type: "marketListing" }>;
}> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const durF = Math.round(scene.durationSec * fps);
  const op = sceneFade(frame, fps, durF);
  const priceScale = spring({
    frame: Math.max(0, frame - Math.round(fps * 0.3)),
    fps,
    config: { damping: 8, stiffness: 140 },
    durationInFrames: 20,
  });

  return (
    <SceneFrame opacity={op}>
      <div style={{ width: "100%", textAlign: "center" }}>
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 10,
            background: "rgba(239,68,68,0.15)",
            border: `1px solid ${COLORS.red}`,
            borderRadius: 8,
            padding: "10px 18px",
            fontFamily,
            color: COLORS.red,
            fontWeight: 800,
            fontSize: 22,
            letterSpacing: 2,
            marginBottom: 28,
          }}
        >
          <LiveDotIcon size={10} color={COLORS.red} /> DARK WEB • {scene.source}
        </div>
        <div
          style={{
            fontFamily,
            color: COLORS.white,
            fontWeight: 900,
            fontSize: 60,
            lineHeight: 1.1,
            marginBottom: 20,
          }}
        >
          {scene.actor}
        </div>
        <div
          style={{
            fontFamily,
            color: COLORS.dim,
            fontSize: 30,
            fontWeight: 500,
            marginBottom: 30,
          }}
        >
          đang rao bán dữ liệu Vercel với giá
        </div>
        <div
          style={{
            fontFamily,
            color: COLORS.red,
            fontSize: 240,
            fontWeight: 900,
            lineHeight: 1,
            letterSpacing: -4,
            transform: `scale(${0.6 + priceScale * 0.4})`,
            textShadow: `0 0 60px ${COLORS.red}`,
          }}
        >
          {scene.price}
        </div>
        {scene.disclaimer && (
          <div
            style={{
              marginTop: 30,
              fontFamily,
              color: COLORS.yellow,
              fontSize: 24,
              fontWeight: 600,
              fontStyle: "italic",
              opacity: priceScale,
            }}
          >
            ⚠ {scene.disclaimer}
          </div>
        )}
      </div>
    </SceneFrame>
  );
};

/* ─────────────────── STEPS scene ─────────────────── */
const StepsScene: React.FC<{
  scene: Extract<NewsScene, { type: "steps" }>;
}> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const durF = Math.round(scene.durationSec * fps);
  const op = sceneFade(frame, fps, durF);
  const per = durF / (scene.steps.length + 1);

  return (
    <SceneFrame opacity={op}>
      <div style={{ width: "100%" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 16,
            marginBottom: 36,
          }}
        >
          <ShieldIcon size={54} color={COLORS.green} />
          <div
            style={{
              fontFamily,
              color: COLORS.white,
              fontWeight: 900,
              fontSize: 50,
              letterSpacing: -0.5,
              textAlign: "center",
            }}
          >
            {scene.title}
          </div>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
          {scene.steps.map((step, i) => {
            const startF = Math.round(per * i);
            const reveal = spring({
              frame: Math.max(0, frame - startF),
              fps,
              config: { damping: 14, stiffness: 100 },
              durationInFrames: 18,
            });
            return (
              <div
                key={i}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 22,
                  background:
                    "linear-gradient(90deg, rgba(34,197,94,0.12), rgba(34,197,94,0.02))",
                  border: `1px solid ${COLORS.green}`,
                  borderRadius: 14,
                  padding: "22px 26px",
                  opacity: reveal,
                  transform: `translateX(${(1 - reveal) * -50}px)`,
                }}
              >
                <div
                  style={{
                    width: 76,
                    height: 76,
                    borderRadius: "50%",
                    background: COLORS.green,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexShrink: 0,
                    boxShadow: `0 0 20px ${COLORS.green}`,
                  }}
                >
                  <div
                    style={{
                      fontFamily,
                      color: "#052E16",
                      fontWeight: 900,
                      fontSize: 42,
                    }}
                  >
                    {i + 1}
                  </div>
                </div>
                <div style={{ flex: 1 }}>
                  <div
                    style={{
                      fontFamily,
                      color: COLORS.white,
                      fontWeight: 800,
                      fontSize: 32,
                      lineHeight: 1.2,
                    }}
                  >
                    {step.label}
                  </div>
                  {step.detail && (
                    <div
                      style={{
                        fontFamily,
                        color: COLORS.dim,
                        fontSize: 22,
                        fontWeight: 500,
                        marginTop: 4,
                      }}
                    >
                      {step.detail}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </SceneFrame>
  );
};

/* ─────────────────── CTA scene ─────────────────── */
const CTAScene: React.FC<{
  scene: Extract<NewsScene, { type: "cta" }>;
}> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const durF = Math.round(scene.durationSec * fps);
  const op = sceneFade(frame, fps, durF);
  const pulse = 0.8 + Math.sin((frame / fps) * 5) * 0.2;

  return (
    <SceneFrame opacity={op}>
      <div style={{ width: "100%", textAlign: "center" }}>
        <div
          style={{
            fontFamily,
            color: COLORS.yellow,
            fontWeight: 900,
            fontSize: 72,
            lineHeight: 1.1,
            marginBottom: 40,
            textShadow: `0 0 30px ${COLORS.yellow}`,
          }}
        >
          {scene.prompt}
        </div>
        <div
          style={{
            display: "inline-block",
            background: `linear-gradient(135deg, ${COLORS.red}, #B91C1C)`,
            padding: "28px 56px",
            borderRadius: 18,
            boxShadow: `0 0 ${pulse * 40}px rgba(239,68,68,0.6)`,
            transform: `scale(${pulse})`,
            marginBottom: 28,
          }}
        >
          <div
            style={{
              fontFamily,
              color: "#fff",
              fontWeight: 900,
              fontSize: 68,
              letterSpacing: 1,
            }}
          >
            {scene.brand}
          </div>
        </div>
        <div
          style={{
            fontFamily,
            color: COLORS.white,
            fontWeight: 600,
            fontSize: 34,
            lineHeight: 1.3,
          }}
        >
          {scene.tagline}
        </div>
      </div>
    </SceneFrame>
  );
};

/* ─────────────────── Main NewsShare component ─────────────────── */
const SceneRouter: React.FC<{ scene: NewsScene }> = ({ scene }) => {
  switch (scene.type) {
    case "hero":
      return <HeroScene scene={scene} />;
    case "stat":
      return <StatScene scene={scene} />;
    case "question":
      return <QuestionScene scene={scene} />;
    case "attackChain":
      return <AttackChainScene scene={scene} />;
    case "leakList":
      return <LeakListScene scene={scene} />;
    case "quote":
      return <QuoteScene scene={scene} />;
    case "marketListing":
      return <MarketListingScene scene={scene} />;
    case "steps":
      return <StepsScene scene={scene} />;
    case "cta":
      return <CTAScene scene={scene} />;
    default:
      return null;
  }
};

export const NewsShare: React.FC<NewsShareProps> = ({
  audioPath,
  breakingLabel = "BREAKING NEWS",
  dateLabel = "19.04.2026",
  brandName = "THE AI FIRST",
  brandTagline = "AI & Security Watch",
  tickerItems,
  scenes,
  captions,
  bgMusicPath,
  bgMusicVolume = 0.08,
}) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ background: COLORS.bg }}>
      <TechBackground />

      {scenes.map((scene, i) => {
        const startF = Math.round(scene.startSec * fps);
        const durF = Math.round(scene.durationSec * fps);
        return (
          <Sequence key={i} from={startF} durationInFrames={durF}>
            <SceneRouter scene={scene} />
          </Sequence>
        );
      })}

      <BreakingBanner breakingLabel={breakingLabel} dateLabel={dateLabel} />
      <BrandIdent brand={brandName} tagline={brandTagline} />
      <CurrentCaption captions={captions} />
      <Ticker items={tickerItems} brand={brandName} />
      <ProgressBar />

      <Audio src={staticFile(audioPath)} />
      {bgMusicPath && (
        <Audio src={staticFile(bgMusicPath)} volume={bgMusicVolume} loop />
      )}
    </AbsoluteFill>
  );
};
