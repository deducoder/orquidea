import React from "react";
import { STAGGER, useEnter } from "../anim";
import { colors, fonts } from "../theme";

export type HeadlineLine = {
  text: string;
  color?: string;
  // Horizontal offset in px (negative lets the line bleed off the frame).
  offset?: number;
  from?: "left" | "right";
  delay?: number;
};

type Props = {
  lines: (string | HeadlineLine)[];
  size?: number;
  color?: string;
  delay?: number;
  stagger?: number;
  maxWidth?: number;
};

const OFFSETS = [0, 56, 18, 84];
const SLIDE_DISTANCE = 1300;

const Line: React.FC<{
  line: HeadlineLine;
  index: number;
  size: number;
  color: string;
  delay: number;
  maxWidth?: number;
}> = ({ line, index, size, color, delay, maxWidth }) => {
  const p = useEnter(line.delay ?? delay);
  const dir = (line.from ?? (index % 2 === 0 ? "left" : "right")) === "left" ? -1 : 1;
  const offset = line.offset ?? OFFSETS[index % OFFSETS.length] * (size / 170);
  return (
    <div
      style={{
        fontFamily: fonts.display,
        fontWeight: 800,
        fontSize: size,
        lineHeight: 0.92,
        letterSpacing: "-0.035em",
        color: line.color ?? color,
        whiteSpace: maxWidth ? "normal" : "nowrap",
        maxWidth,
        transform: `translateX(${offset + (1 - p) * SLIDE_DISTANCE * dir}px)`,
        opacity: Math.min(1, p * 4),
      }}
    >
      {line.text}
    </div>
  );
};

// Staggered lines of extra bold display type that slide in with a spring.
export const Headline: React.FC<Props> = ({
  lines,
  size = 170,
  color = colors.blanco,
  delay = 0,
  stagger = STAGGER,
  maxWidth,
}) => (
  <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-start" }}>
    {lines.map((l, i) => (
      <Line
        key={i}
        index={i}
        size={size}
        color={color}
        delay={delay + i * stagger}
        maxWidth={maxWidth}
        line={typeof l === "string" ? { text: l } : l}
      />
    ))}
  </div>
);
