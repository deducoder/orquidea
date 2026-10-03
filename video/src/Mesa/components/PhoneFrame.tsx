import React from "react";
import { useEnter, useLoop } from "../anim";
import { colors, radii, springs } from "../theme";

export const PHONE_W = 440;
export const PHONE_H = 900;

type Props = {
  variant?: "light" | "dark";
  tilt?: { x?: number; y?: number; z?: number };
  scale?: number;
  delay?: number;
  floatAmp?: number;
  floatPeriod?: number;
  phase?: number;
  from?: "bottom" | "right" | "left";
  children?: React.ReactNode;
};

// CSS-drawn phone. Occupies PHONE_W*scale x PHONE_H*scale in layout; the 3D
// tilt, float loop and entrance are transforms around its centre.
export const PhoneFrame: React.FC<Props> = ({
  variant = "light",
  tilt = {},
  scale = 1,
  delay = 0,
  floatAmp = 14,
  floatPeriod = 3.4,
  phase = 0,
  from = "bottom",
  children,
}) => {
  const p = useEnter(delay, 18, springs.soft);
  const loop = useLoop(floatPeriod, phase);
  const dark = variant === "dark";
  const enter = (1 - p) * 1100;
  const tx = from === "right" ? enter : from === "left" ? -enter : 0;
  const ty = from === "bottom" ? enter : 0;
  const rx = (tilt.x ?? 6) + loop * 1.2;
  const ry = (tilt.y ?? -12) + loop * 1.6;
  const rz = tilt.z ?? 0;

  return (
    <div
      style={{
        position: "relative",
        width: PHONE_W * scale,
        height: PHONE_H * scale,
        flex: "none",
      }}
    >
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "50%",
          width: PHONE_W,
          height: PHONE_H,
          marginLeft: -PHONE_W / 2,
          marginTop: -PHONE_H / 2,
          boxSizing: "border-box",
          padding: 12,
          borderRadius: radii.phone,
          background: dark ? "#2A2A2E" : colors.blanco,
          boxShadow: "0 50px 90px rgba(0,0,0,0.28)",
          transform: `perspective(1800px) translate3d(${tx}px, ${ty + loop * floatAmp}px, 0) rotateX(${rx}deg) rotateY(${ry}deg) rotateZ(${rz}deg) scale(${scale})`,
        }}
      >
        <div
          style={{
            position: "relative",
            width: "100%",
            height: "100%",
            boxSizing: "border-box",
            borderRadius: radii.screen,
            background: dark ? colors.negro : colors.crema,
            overflow: "hidden",
          }}
        >
          <div
            style={{
              position: "absolute",
              top: 16,
              left: "50%",
              width: 120,
              height: 30,
              marginLeft: -60,
              borderRadius: 15,
              background: dark ? "#2A2A2E" : colors.negro,
              zIndex: 2,
            }}
          />
          <div
            style={{
              position: "absolute",
              inset: 0,
              boxSizing: "border-box",
              padding: "66px 20px 20px",
              display: "flex",
              flexDirection: "column",
            }}
          >
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};
