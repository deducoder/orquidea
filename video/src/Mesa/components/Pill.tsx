import React from "react";
import { colors, fonts, radii } from "../theme";

type Props = {
  children: React.ReactNode;
  bg?: string;
  color?: string;
  size?: number;
  style?: React.CSSProperties;
};

export const Pill: React.FC<Props> = ({
  children,
  bg = colors.negro,
  color = colors.blanco,
  size = 26,
  style,
}) => (
  <div
    style={{
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      gap: size * 0.3,
      padding: `${size * 0.4}px ${size * 0.95}px`,
      borderRadius: radii.pill,
      background: bg,
      color,
      fontFamily: fonts.ui,
      fontWeight: 700,
      fontSize: size,
      lineHeight: 1,
      whiteSpace: "nowrap",
      ...style,
    }}
  >
    {children}
  </div>
);
