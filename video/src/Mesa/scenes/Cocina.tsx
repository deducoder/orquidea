import React from "react";
import { interpolateColors, useCurrentFrame } from "remotion";
import { Headline } from "../components/Headline";
import { PhoneFrame } from "../components/PhoneFrame";
import { Pill } from "../components/Pill";
import { SceneLayout, useLayout } from "../layout";
import { pulse, ramp, useEnter, useLoop } from "../anim";
import type { MesaProps } from "../data";
import { colors, fonts, radii } from "../theme";

const CARD_AT = [20, 42, 64];
const FLIP_AT = 104;

const Comanda: React.FC<{
  c: MesaProps["cocina"]["comandas"][number];
  d: MesaProps["cocina"];
  index: number;
}> = ({ c, d, index }) => {
  const frame = useCurrentFrame();
  const p = useEnter(CARD_AT[index] ?? 0);
  const flips = index === 0;
  const badge = useLoop(0.9);
  const isNewest = index === d.comandas.length - 1;
  const status = flips ? ramp(frame, FLIP_AT, FLIP_AT + 8) : 0;
  const bg = interpolateColors(status, [0, 1], [colors.amarillo, colors.verde]);
  const label = status > 0.5 ? d.listo : d.pagado;
  return (
    <div
      style={{
        position: "relative",
        borderRadius: radii.card,
        background: colors.grisOscuro,
        padding: "22px 24px",
        marginBottom: 14,
        opacity: Math.min(1, p * 3),
        transform: `translateY(${(1 - p) * -260}px) scale(${flips ? pulse(frame, FLIP_AT, 0.06, 10) : 1})`,
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ fontFamily: fonts.display, fontWeight: 800, fontSize: 46, color: colors.blanco, letterSpacing: "-0.04em" }}>
          {c.id}
        </div>
        <Pill size={22} bg={bg} color={colors.negro}>
          {label}
        </Pill>
      </div>
      <div style={{ fontFamily: fonts.ui, fontWeight: 500, fontSize: 26, color: "#B9B4AA", marginTop: 8 }}>
        {c.detalle}
      </div>
      {isNewest && frame >= (CARD_AT[index] ?? 0) + 8 ? (
        <div style={{ position: "absolute", left: 22, top: -16, transform: `scale(${1 + badge * 0.07})` }}>
          <Pill size={20} bg={colors.tomate} color={colors.blanco}>
            {d.nuevo}
          </Pill>
        </div>
      ) : null}
    </div>
  );
};

const CocinaPhone: React.FC<{ d: MesaProps["cocina"] }> = ({ d }) => (
  <>
    <div style={{ fontFamily: fonts.display, fontWeight: 800, fontSize: 44, color: colors.blanco, letterSpacing: "-0.04em", marginBottom: 26 }}>
      {d.encabezado}
    </div>
    {d.comandas.map((c, i) => (
      <Comanda key={c.id} c={c} d={d} index={i} />
    ))}
  </>
);

export const Cocina: React.FC<{ props: MesaProps }> = ({ props }) => {
  const { vertical } = useLayout();
  const d = props.cocina;
  return (
    <SceneLayout
      bg={colors.negro}
      text={
        <Headline
          lines={d.lineas.map((text, i) => ({ text, color: i === 0 ? colors.blanco : colors.verde }))}
          size={vertical ? 190 : 190}
        />
      }
      visual={
        <PhoneFrame scale={vertical ? 1.15 : 1} variant="dark" tilt={{ x: 6, y: 12 }} delay={6} from="right" floatPeriod={3.5} phase={0.6}>
          <CocinaPhone d={d} />
        </PhoneFrame>
      }
    />
  );
};
