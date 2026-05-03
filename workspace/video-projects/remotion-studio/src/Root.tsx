import React from "react";
import { Composition } from "remotion";
import { DarkMinimal } from "./templates/DarkMinimal";
import { BoldHighlight } from "./templates/BoldHighlight";
import { EpicFullscreen } from "./templates/EpicFullscreen";
import { ImageKenBurns } from "./templates/ImageKenBurns";
import { ProgressiveReduction } from "./templates/ProgressiveReduction";
import { HeyGenShort } from "./templates/HeyGenShort";
import { PromptTyping } from "./templates/PromptTyping";
import { TikTokCreator } from "./templates/TikTokCreator";
import { NewsShare } from "./templates/NewsShare";
import type {
  DarkMinimalProps,
  BoldHighlightProps,
  EpicFullscreenProps,
  ImageKenBurnsProps,
  ProgressiveReductionProps,
  HeyGenShortProps,
  PromptTypingProps,
  TikTokCreatorProps,
  NewsShareProps,
} from "./types";

const FPS = 30;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition<DarkMinimalProps>
        id="DarkMinimal"
        component={DarkMinimal}
        fps={FPS}
        width={1080}
        height={1920}
        durationInFrames={8 * FPS}
        calculateMetadata={({ props }) => ({
          durationInFrames: (props.durationSeconds ?? 8) * FPS,
        })}
        defaultProps={{
          title: "Title here",
          items: ["Item 1", "Item 2"],
          watermark: "@tranvanhoang.com",
          bgVideo: "media/videos/bg.mp4",
        }}
      />

      <Composition<BoldHighlightProps>
        id="BoldHighlight"
        component={BoldHighlight}
        fps={FPS}
        width={1080}
        height={1920}
        durationInFrames={10 * FPS}
        calculateMetadata={({ props }) => ({
          durationInFrames: (props.durationSeconds ?? 10) * FPS,
        })}
        defaultProps={{
          title: "Title here",
          bodyLines: [{ text: "Body line 1" }],
          watermark: "@tranvanhoang.com",
          bgVideo: "media/videos/bg.mp4",
        }}
      />

      <Composition<EpicFullscreenProps>
        id="EpicFullscreen"
        component={EpicFullscreen}
        fps={FPS}
        width={1080}
        height={1920}
        durationInFrames={8 * FPS}
        calculateMetadata={({ props }) => ({
          durationInFrames: (props.durationSeconds ?? 8) * FPS,
        })}
        defaultProps={{
          lines: [{ text: "Line 1" }],
          bgVideo: "media/videos/bg.mp4",
        }}
      />

      <Composition<ImageKenBurnsProps>
        id="ImageKenBurns"
        component={ImageKenBurns}
        fps={FPS}
        width={1080}
        height={1080}
        durationInFrames={8 * FPS}
        calculateMetadata={({ props }) => ({
          durationInFrames: (props.durationSeconds ?? 8) * FPS,
        })}
        defaultProps={{
          imagePath: "media/image.png",
        }}
      />

      <Composition<ProgressiveReductionProps>
        id="ProgressiveReduction"
        component={ProgressiveReduction}
        fps={FPS}
        width={1080}
        height={1920}
        durationInFrames={18 * FPS}
        calculateMetadata={({ props }) => ({
          durationInFrames: props.durationSeconds * FPS,
        })}
        defaultProps={{
          durationSeconds: 18,
          watermark: "@tranvanhoang.com",
          bgVideo: "media/videos/bg.mp4",
          sections: [],
        }}
      />
      <Composition<PromptTypingProps>
        id="PromptTyping"
        component={PromptTyping}
        fps={FPS}
        width={1080}
        height={1920}
        durationInFrames={12 * FPS}
        calculateMetadata={({ props }) => ({
          durationInFrames: Math.round(props.durationSeconds * FPS),
        })}
        defaultProps={{
          text: "Tôi muốn bạn hiểu rõ về tôi...",
          durationSeconds: 12,
        }}
      />
      <Composition<TikTokCreatorProps>
        id="TikTokCreator"
        component={TikTokCreator}
        fps={FPS}
        width={1080}
        height={1920}
        durationInFrames={97 * FPS}
        calculateMetadata={({ props }) => ({
          durationInFrames: Math.round(props.durationSeconds * FPS),
        })}
        defaultProps={require("../props/tiktok-creator.json")}
      />

      <Composition<NewsShareProps>
        id="NewsShare"
        component={NewsShare}
        fps={FPS}
        width={1080}
        height={1920}
        durationInFrames={95 * FPS}
        calculateMetadata={({ props }) => ({
          durationInFrames: Math.round(props.durationSeconds * FPS),
        })}
        defaultProps={require("../props/news-share-vercel.json")}
      />

      <Composition<HeyGenShortProps>
        id="HeyGenShort"
        component={HeyGenShort}
        fps={FPS}
        width={1080}
        height={1920}
        durationInFrames={40 * FPS}
        calculateMetadata={({ props }) => ({
          durationInFrames: Math.round(
            (props.durationSeconds + (props.outro?.durationSeconds ?? 0)) * FPS
          ),
        })}
        defaultProps={require("../props/heygen-short.json")}
      />
    </>
  );
};
