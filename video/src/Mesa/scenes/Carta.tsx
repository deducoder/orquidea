import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Headline } from "../components/Headline";
import { ICONS, QR } from "../components/Illustrations";
import { PhoneFrame } from "../components/PhoneFrame";
import { Pill } from "../components/Pill";
import { SceneLayout, useLayout } from "../layout";
import { pulse, useEnter } from "../anim";
import type { MesaProps } from "../data";
import { colors, fonts, radii, springs } from "../theme";

const ADD_AT = [38, 56, 74];
const DAY_AT = 104;
const DAY_STEP = 79;

const Card: React.FC<{
  p: MesaProps["carta"]["productos"][number];
  index: number;
}> = ({ p, index }) => {
  const frame = useCurrentFrame();
  const enter = useEnter(12 + index * 4);
  const Icon = ICONS[p.icono];
  const added = ADD_AT[index] ?? -1000;
  return (
    <div
      style={{
        flex: 1,
        height: 200,
        borderRadius: radii.card,
        background: colors[p.tono],
        padding: 14,
        boxSizing: "border-box",
        position: "relative",
        transform: `scale(${enter})`,
        color: p.tono === "cobalto" ? colors.blanco : colors.negro,
      }}
    >
      <Icon
        size={84}
        color={p.tono === "cobalto" ? colors.crema : colors.blanco}
        accent={colors.negro}
      />
      <div style={{ fontFamily: fonts.display, fontWeight: 800, fontSize: 30, marginTop: 6, letterSpacing: "-0.03em" }}>
        {p.nombre}
      </div>
      <div style={{ fontFamily: fonts.ui, fontWeight: 700, fontSize: 24 }}>${p.precio}</div>
      <div
        style={{
          position: "absolute",
          right: 12,
          bottom: 12,
          width: 46,
          height: 46,
          borderRadius: 23,
          background: colors.negro,
          color: colors.blanco,
          fontFamily: fonts.ui,
          fontWeight: 700,
          fontSize: 34,
          lineHeight: "44px",
          textAlign: "center",
          transform: `scale(${pulse(frame, added, 0.35, 10)})`,
        }}
      >
        +
      </div>
    </div>
  );
};

const CartaPhone: React.FC<{ d: MesaProps["carta"]; brand: string }> = ({ d, brand }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const items = d.productos.slice(0, ADD_AT.length);
  const count = ADD_AT.filter((a) => frame >= a).length;

  // Cumulative total, each addition eased over 8 frames.
  const input: number[] = [0];
  const output: number[] = [0];
  let sum = 0;
  items.forEach((it, i) => {
    input.push(ADD_AT[i], ADD_AT[i] + 8);
    output.push(sum, sum + it.precio);
    sum += it.precio;
  });
  const total = interpolate(frame, input, output, {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const sel = spring({ frame, fps, delay: DAY_AT, durationInFrames: 14, config: springs.snappy });
  const cartIn = useEnter(30);

  return (
    <>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ fontFamily: fonts.display, fontWeight: 800, fontSize: 38, letterSpacing: "-0.05em" }}>
          {brand}
        </div>
        <Pill bg={colors.gris} color={colors.negro} size={20}>
          Mesa 4
        </Pill>
      </div>
      <div style={{ display: "flex", gap: 8, marginTop: 18 }}>
        {d.categorias.map((c, i) => (
          <Pill key={c} size={20} bg={i === 0 ? colors.negro : colors.gris} color={i === 0 ? colors.blanco : colors.negro}>
            {c}
          </Pill>
        ))}
      </div>
      <div style={{ display: "flex", gap: 12, marginTop: 18 }}>
        <Card p={d.productos[0]} index={0} />
        <Card p={d.productos[1]} index={1} />
      </div>
      <div style={{ display: "flex", gap: 12, marginTop: 12 }}>
        <Card p={d.productos[2]} index={2} />
        <Card p={d.productos[3]} index={3} />
      </div>
      <div style={{ position: "relative", height: 64, marginTop: 22 }}>
        <div
          style={{
            position: "absolute",
            left: sel * d.diaElegido * DAY_STEP,
            top: 0,
            width: 64,
            height: 64,
            borderRadius: 32,
            background: colors.negro,
          }}
        />
        {d.dias.map((day, i) => {
          const active = Math.abs(sel * d.diaElegido - i) < 0.5;
          return (
            <div
              key={day}
              style={{
                position: "absolute",
                left: i * DAY_STEP,
                top: 0,
                width: 64,
                height: 64,
                borderRadius: 32,
                background: active ? "transparent" : colors.gris,
                color: active ? colors.blanco : colors.negro,
                fontFamily: fonts.display,
                fontWeight: 800,
                fontSize: 28,
                lineHeight: "64px",
                textAlign: "center",
                zIndex: 1,
              }}
            >
              {day}
            </div>
          );
        })}
      </div>
      <div style={{ flex: 1 }} />
      <div
        style={{
          height: 84,
          borderRadius: 42,
          background: colors.negro,
          color: colors.blanco,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 14px 0 30px",
          fontFamily: fonts.ui,
          fontWeight: 700,
          fontSize: 28,
          transform: `translateY(${(1 - cartIn) * 140}px)`,
        }}
      >
        <span>{d.carrito}</span>
        <span style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <span
            style={{
              width: 44,
              height: 44,
              borderRadius: 22,
              background: colors.verde,
              color: colors.negro,
              textAlign: "center",
              lineHeight: "44px",
              transform: `scale(${count === 0 ? 0 : pulse(frame, ADD_AT[count - 1], 0.4, 10)})`,
            }}
          >
            {count}
          </span>
          <span style={{ fontVariantNumeric: "tabular-nums" }}>${Math.round(total)}</span>
        </span>
      </div>
    </>
  );
};

export const Carta: React.FC<{ props: MesaProps }> = ({ props }) => {
  const { vertical } = useLayout();
  const d = props.carta;
  const labelIn = useEnter(16);
  return (
    <SceneLayout
      bg={colors.crema}
      text={
        <>
          <Headline lines={[d.titular]} size={vertical ? 220 : 240} color={colors.negro} />
          <div
            style={{
              marginTop: 36,
              display: "inline-flex",
              alignItems: "center",
              gap: 26,
              alignSelf: "flex-start",
              background: colors.blanco,
              borderRadius: radii.card,
              padding: "20px 34px 20px 20px",
              fontFamily: fonts.display,
              fontWeight: 800,
              fontSize: 42,
              lineHeight: 1,
              letterSpacing: "-0.03em",
              maxWidth: vertical ? 800 : 780,
              transform: `translateX(${(1 - labelIn) * -900}px)`,
            }}
          >
            <QR size={110} />
            <span>{d.etiqueta}</span>
          </div>
        </>
      }
      visual={
        <PhoneFrame scale={vertical ? 1.15 : 1} variant="light" tilt={{ x: 6, y: -12 }} delay={6} floatPeriod={3.6}>
          <CartaPhone d={d} brand={props.marca} />
        </PhoneFrame>
      }
    />
  );
};
