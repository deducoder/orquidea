import React from "react";
import { useCurrentFrame } from "remotion";
import { Counter } from "../components/Counter";
import { Headline } from "../components/Headline";
import { Check } from "../components/Illustrations";
import { PhoneFrame } from "../components/PhoneFrame";
import { SceneLayout, useLayout } from "../layout";
import { pulse, ramp, useEnter } from "../anim";
import type { MesaProps } from "../data";
import { colors, fonts } from "../theme";

const PRESS_AT = 62;
const CONFIRM_AT = 70;

const Row: React.FC<{ name: string; price: number; index: number }> = ({ name, price, index }) => {
  const p = useEnter(16 + index * 6);
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        fontFamily: fonts.ui,
        fontWeight: 700,
        fontSize: 30,
        padding: "20px 0",
        borderBottom: `3px solid ${colors.gris}`,
        opacity: Math.min(1, p * 3),
        transform: `translateX(${(1 - p) * 120}px)`,
      }}
    >
      <span>{name}</span>
      <span>${price}</span>
    </div>
  );
};

const PagoPhone: React.FC<{ d: MesaProps["pago"] }> = ({ d }) => {
  const frame = useCurrentFrame();
  const total = d.resumen.reduce((a, r) => a + r.precio, 0);
  const confirm = useEnter(CONFIRM_AT);
  const btnOut = ramp(frame, CONFIRM_AT - 2, CONFIRM_AT + 6, 1, 0);
  const check = ramp(frame, CONFIRM_AT + 6, CONFIRM_AT + 20);
  return (
    <>
      <div style={{ fontFamily: fonts.display, fontWeight: 800, fontSize: 44, letterSpacing: "-0.04em" }}>
        {d.encabezado}
      </div>
      <div style={{ marginTop: 14 }}>
        {d.resumen.map((r, i) => (
          <Row key={r.nombre} name={r.nombre} price={r.precio} index={i} />
        ))}
      </div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          fontFamily: fonts.display,
          fontWeight: 800,
          fontSize: 44,
          marginTop: 28,
          letterSpacing: "-0.03em",
        }}
      >
        <span>{d.total}</span>
        <Counter to={total} start={28} duration={22} prefix="$" />
      </div>
      <div style={{ flex: 1 }} />
      <div style={{ position: "relative", height: 150 }}>
        <div
          style={{
            position: "absolute",
            inset: "auto 0 0 0",
            height: 92,
            borderRadius: 46,
            background: colors.verde,
            color: colors.negro,
            fontFamily: fonts.ui,
            fontWeight: 700,
            fontSize: 28,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            opacity: btnOut,
            transform: `scale(${pulse(frame, PRESS_AT, -0.07, 8)})`,
          }}
        >
          {d.boton}
        </div>
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 14,
            fontFamily: fonts.display,
            fontWeight: 800,
            fontSize: 32,
            whiteSpace: "nowrap",
            letterSpacing: "-0.03em",
            transform: `scale(${confirm})`,
            opacity: Math.min(1, confirm * 3),
          }}
        >
          <Check size={72} progress={check} />
          <span>{d.confirmado}</span>
        </div>
      </div>
    </>
  );
};

export const Pago: React.FC<{ props: MesaProps }> = ({ props }) => {
  const { vertical } = useLayout();
  const d = props.pago;
  return (
    <SceneLayout
      bg={colors.cobalto}
      text={
        <Headline
          lines={d.lineas.map((text, i) => ({ text, color: i === 0 ? colors.blanco : colors.amarillo }))}
          size={vertical ? 230 : 220}
        />
      }
      visual={
        <PhoneFrame scale={vertical ? 1.15 : 1} variant="light" tilt={{ x: 5, y: 12 }} delay={6} from="right" floatPeriod={3.2} phase={1}>
          <PagoPhone d={d} />
        </PhoneFrame>
      }
    />
  );
};
