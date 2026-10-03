import React from "react";
import { Img } from "remotion";
import { colors, fonts } from "../theme";

type Props = { brand: string; logo?: string; size?: number; color?: string };

// Provisional text wordmark; pass `logo` to swap in an image.
export const Wordmark: React.FC<Props> = ({
  brand,
  logo,
  size = 120,
  color = colors.crema,
}) =>
  logo ? (
    <Img src={logo} style={{ height: size, display: "block" }} />
  ) : (
    <div
      style={{
        fontFamily: fonts.display,
        fontWeight: 800,
        fontSize: size,
        lineHeight: 1,
        letterSpacing: "-0.05em",
        color,
      }}
    >
      {brand}
    </div>
  );
