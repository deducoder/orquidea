import React from "react";
import { useCurrentFrame } from "remotion";
import { Chip } from "../components/Chip";
import { Headline } from "../components/Headline";
import { PhoneFrame } from "../components/PhoneFrame";
import { SceneLayout, useLayout } from "../layout";
import { ramp, useEnter } from "../anim";
import type { MesaProps } from "../data";
import { colors, fonts } from "../theme";

const TYPING_AT = 18;
const BUBBLE_AT = 46;

const Typing: React.FC = () => {
  const frame = useCurrentFrame();
  const out = ramp(frame, BUBBLE_AT - 4, BUBBLE_AT, 1, 0);
  const inn = ramp(frame, TYPING_AT, TYPING_AT + 8);
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        display: "flex",
        gap: 10,
        padding: "22px 26px",
        borderRadius: 30,
        background: colors.blanco,
        opacity: Math.min(inn, out),
      }}
    >
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          style={{
            width: 16,
            height: 16,
            borderRadius: 8,
            background: colors.grisMedio,
            transform: `translateY(${-Math.abs(Math.sin((frame - i * 4) / 5)) * 10}px)`,
          }}
        />
      ))}
    </div>
  );
};

const ChatPhone: React.FC<{ d: MesaProps["whatsapp"]; brand: string }> = ({ d, brand }) => {
  const b = useEnter(BUBBLE_AT);
  return (
    <>
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <div
          style={{
            width: 62,
            height: 62,
            borderRadius: 31,
            background: colors.tomate,
            color: colors.crema,
            fontFamily: fonts.display,
            fontWeight: 800,
            fontSize: 36,
            textAlign: "center",
            lineHeight: "62px",
          }}
        >
          {brand.charAt(0)}
        </div>
        <div style={{ fontFamily: fonts.ui, fontWeight: 700, fontSize: 32 }}>{brand}</div>
      </div>
      <div style={{ position: "relative", marginTop: 40 }}>
        <Typing />
        <div
          style={{
            width: 340,
            padding: "24px 26px",
            borderRadius: "30px 30px 30px 8px",
            background: colors.blanco,
            transformOrigin: "0% 100%",
            transform: `scale(${b})`,
            opacity: Math.min(1, b * 4),
            fontFamily: fonts.ui,
            fontSize: 28,
            lineHeight: 1.3,
          }}
        >
          <div style={{ fontFamily: fonts.display, fontWeight: 800, fontSize: 38, letterSpacing: "-0.03em" }}>
            {d.pedido}
          </div>
          <div style={{ fontWeight: 700, marginTop: 10 }}>
            {d.dia} · {d.hora}
          </div>
          <div style={{ color: colors.grisMedio, marginTop: 6 }}>{d.resumen}</div>
        </div>
      </div>
    </>
  );
};

export const Whatsapp: React.FC<{ props: MesaProps }> = ({ props }) => {
  const { vertical } = useLayout();
  const d = props.whatsapp;
  return (
    <SceneLayout
      bg={colors.rosa}
      text={<Headline lines={d.lineas} size={vertical ? 150 : 150} color={colors.negro} />}
      visual={
        <div style={{ position: "relative" }}>
          <PhoneFrame variant="light" tilt={{ x: 6, y: -12 }} delay={6} floatPeriod={3.8}>
            <ChatPhone d={d} brand={props.marca} />
          </PhoneFrame>
          <Chip bg={colors.negro} color={colors.crema} size={46} rotate={-8} delay={64} style={{ left: -60, top: 120 }}>
            {d.pedido.replace(/^\D+/, "")}
          </Chip>
          <Chip bg={colors.amarillo} size={42} rotate={7} delay={74} phase={2} style={{ right: -70, bottom: 150 }}>
            {d.hora}
          </Chip>
        </div>
      }
    />
  );
};
