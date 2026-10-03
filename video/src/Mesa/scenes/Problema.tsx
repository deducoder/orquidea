import React from "react";
import { useCurrentFrame } from "remotion";
import { Headline } from "../components/Headline";
import { SceneLayout, useLayout } from "../layout";
import { ramp } from "../anim";
import type { MesaProps } from "../data";
import { colors } from "../theme";

// One word per beat, 22 frames apart.
const BEAT = 22;
const COLORS = [colors.blanco, colors.tomate, colors.amarillo];

const Queue: React.FC = () => {
  const frame = useCurrentFrame();
  const { vertical } = useLayout();
  const n = vertical ? 9 : 14;
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom: vertical ? 170 : 90,
        display: "flex",
        gap: 24,
        paddingLeft: vertical ? 72 : 110,
      }}
    >
      {Array.from({ length: n }).map((_, i) => {
        const p = ramp(frame, 8 + i * 3, 22 + i * 3);
        return (
          <div
            key={i}
            style={{
              width: 54,
              height: 54,
              borderRadius: 27,
              background: i === 0 ? colors.tomate : colors.grisOscuro,
              transform: `scale(${p})`,
            }}
          />
        );
      })}
    </div>
  );
};

export const Problema: React.FC<{ props: MesaProps }> = ({ props }) => {
  const { vertical } = useLayout();
  const lines = props.problema.lineas.map((text, i) => ({
    text,
    color: COLORS[i % COLORS.length],
    delay: 6 + i * BEAT,
  }));
  return (
    <SceneLayout
      bg={colors.negro}
      text={
        <>
          <Headline lines={lines} size={vertical ? 190 : 200} maxWidth={vertical ? 650 : 1600} />
          <Queue />
        </>
      }
    />
  );
};
