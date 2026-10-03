import React from "react";
import { useEnter, useLoop } from "../anim";
import { colors, fonts, radii } from "../theme";

type Props = {
  children: React.ReactNode;
  bg?: string;
  color?: string;
  size?: number;
  rotate?: number;
  delay?: number;
  phase?: number;
  style?: React.CSSProperties;
};

// Flat tag that pops in, then bobs and rocks slightly.
export const Chip: React.FC<Props> = ({
  children,
  bg = colors.amarillo,
  color = colors.negro,
  size = 40,
  rotate = -6,
  delay = 0,
  phase = 0,
  style,
}) => {
  const p = useEnter(delay);
  const loop = useLoop(2.6, phase);
  return (
    <div
      style={{
        position: "absolute",
        padding: `${size * 0.35}px ${size * 0.7}px`,
        borderRadius: radii.chip,
        background: bg,
        color,
        fontFamily: fonts.display,
        fontWeight: 800,
        fontSize: size,
        lineHeight: 1,
        letterSpacing: "-0.03em",
        whiteSpace: "nowrap",
        transform: `translateY(${loop * 8}px) rotate(${rotate + loop * 2.5}deg) scale(${p})`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};
