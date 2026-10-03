import React from "react";
import { AbsoluteFill, useVideoConfig } from "remotion";

export const useLayout = () => {
  const { width, height } = useVideoConfig();
  return { width, height, vertical: height > width };
};

type Props = {
  bg: string;
  text?: React.ReactNode;
  visual?: React.ReactNode;
};

// One layout for both formats: text above visual when vertical, side by side
// when horizontal. Design units are px of a 1080 short side in both.
export const SceneLayout: React.FC<Props> = ({ bg, text, visual }) => {
  const { vertical } = useLayout();
  return (
    <AbsoluteFill style={{ background: bg, overflow: "hidden" }}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: vertical ? "column" : "row",
          padding: vertical ? "170px 72px 60px" : "0 110px",
        }}
      >
        <div
          style={{
            flex: vertical && visual ? "0 0 auto" : "1 1 0",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            minWidth: 0,
          }}
        >
          {text}
        </div>
        {visual ? (
          <div
            style={{
              flex: "1 1 0",
              position: "relative",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              minWidth: 0,
              minHeight: 0,
            }}
          >
            {visual}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};
