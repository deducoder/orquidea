import React from "react";
import { useCurrentFrame } from "remotion";
import { ramp } from "../anim";

type Props = {
  to: number;
  from?: number;
  start?: number;
  duration?: number;
  prefix?: string;
  suffix?: string;
  style?: React.CSSProperties;
};

export const Counter: React.FC<Props> = ({
  to,
  from = 0,
  start = 0,
  duration = 24,
  prefix = "",
  suffix = "",
  style,
}) => {
  const frame = useCurrentFrame();
  const v = ramp(frame, start, start + duration, from, to);
  return (
    <span style={{ fontVariantNumeric: "tabular-nums", ...style }}>
      {prefix}
      {Math.round(v)}
      {suffix}
    </span>
  );
};
