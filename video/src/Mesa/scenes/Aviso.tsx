import React from "react";
import { useCurrentFrame } from "remotion";
import { Headline } from "../components/Headline";
import { PhoneFrame } from "../components/PhoneFrame";
import { SceneLayout, useLayout } from "../layout";
import { pulse, ramp, useEnter } from "../anim";
import type { MesaProps } from "../data";
import { colors, fonts, radii } from "../theme";

const TAP_AT = 24;
const BUBBLE_AT = 36;

const AvisoPhone: React.FC<{ d: MesaProps["aviso"] }> = ({ d }) => {
  const frame = useCurrentFrame();
  const card = useEnter(10);
  const bubble = useEnter(BUBBLE_AT);
  const ripple = ramp(frame, TAP_AT, TAP_AT + 14);
  const finger = ramp(frame, TAP_AT - 10, TAP_AT, 1, 0);
  return (
    <>
      <div
        style={{
          borderRadius: radii.card,
          background: colors.grisOscuro,
          padding: "24px",
          transform: `scale(${card})`,
        }}
      >
        <div style={{ fontFamily: fonts.display, fontWeight: 800, fontSize: 52, color: colors.blanco, letterSpacing: "-0.04em" }}>
          {d.pedido}
        </div>
        <div style={{ position: "relative", marginTop: 20 }}>
          <div
            style={{
              height: 84,
              borderRadius: 42,
              background: colors.verde,
              color: colors.negro,
              fontFamily: fonts.ui,
              fontWeight: 700,
              fontSize: 32,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              transform: `scale(${pulse(frame, TAP_AT, -0.08, 8)})`,
            }}
          >
            {d.boton}
          </div>
          <div
            style={{
              position: "absolute",
              left: "50%",
              top: "50%",
              width: 120,
              height: 120,
              marginLeft: -60,
              marginTop: -60,
              borderRadius: 60,
              border: `5px solid ${colors.blanco}`,
              opacity: (1 - ripple) * (frame >= TAP_AT ? 1 : 0),
              transform: `scale(${0.4 + ripple})`,
            }}
          />
          <div
            style={{
              position: "absolute",
              left: "50%",
              top: "50%",
              width: 46,
              height: 46,
              marginLeft: -23 + finger * 60,
              marginTop: -23 + finger * 90,
              borderRadius: 23,
              background: "rgba(255,255,255,0.85)",
              opacity: frame < TAP_AT + 6 ? 1 : 0,
            }}
          />
        </div>
      </div>
      <div
        style={{
          marginTop: 36,
          alignSelf: "flex-end",
          maxWidth: 330,
          padding: "24px 28px",
          borderRadius: "30px 30px 8px 30px",
          background: colors.verde,
          color: colors.negro,
          fontFamily: fonts.ui,
          fontWeight: 700,
          fontSize: 32,
          lineHeight: 1.25,
          transformOrigin: "100% 100%",
          transform: `scale(${bubble})`,
          opacity: Math.min(1, bubble * 4),
        }}
      >
        {d.mensaje}
      </div>
    </>
  );
};

export const Aviso: React.FC<{ props: MesaProps }> = ({ props }) => {
  const { vertical } = useLayout();
  const d = props.aviso;
  return (
    <SceneLayout
      bg={colors.verde}
      text={<Headline lines={d.lineas} size={vertical ? 180 : 170} color={colors.negro} />}
      visual={
        <PhoneFrame variant="dark" tilt={{ x: 5, y: -12 }} delay={4} floatPeriod={3.3}>
          <AvisoPhone d={d} />
        </PhoneFrame>
      }
    />
  );
};
