import React from "react";
import { useCurrentFrame } from "remotion";
import { Counter } from "../components/Counter";
import { Headline } from "../components/Headline";
import { Eye, Pencil } from "../components/Illustrations";
import { PhoneFrame } from "../components/PhoneFrame";
import { Pill } from "../components/Pill";
import { SceneLayout, useLayout } from "../layout";
import { ramp } from "../anim";
import type { MesaProps } from "../data";
import { colors, fonts, radii } from "../theme";

type D = MesaProps["admin"];

const Title: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div style={{ fontFamily: fonts.display, fontWeight: 800, fontSize: 44, letterSpacing: "-0.04em", marginBottom: 22 }}>
    {children}
  </div>
);

const Productos: React.FC<{ d: D["productos"] }> = ({ d }) => {
  const frame = useCurrentFrame();
  const hide = ramp(frame, 50, 58);
  return (
    <>
      <Title>{d.encabezado}</Title>
      {d.items.map((name, i) => {
        const hidden = i === 1;
        const fade = hidden ? 1 - hide * 0.65 : 1;
        return (
          <div
            key={name}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              height: 92,
              borderRadius: radii.card,
              background: colors.blanco,
              padding: "0 20px",
              marginBottom: 12,
              fontFamily: fonts.ui,
              fontWeight: 700,
              fontSize: 30,
            }}
          >
            <span style={{ opacity: fade }}>{name}</span>
            <span style={{ display: "flex", gap: 18 }}>
              <Eye size={44} off={hidden && hide > 0.5} />
              <Pencil size={44} />
            </span>
          </div>
        );
      })}
      <div style={{ flex: 1 }} />
      <Pill size={30} bg={colors.verde} color={colors.negro} style={{ height: 76 }}>
        + {d.alta}
      </Pill>
    </>
  );
};

const Horarios: React.FC<{ d: D["horarios"] }> = ({ d }) => {
  const frame = useCurrentFrame();
  const closed = ramp(frame, 60, 68);
  return (
    <>
      <Title>{d.encabezado}</Title>
      {d.dias.map((day, i) => {
        const isClosed = i === d.diaCerrado;
        return (
          <div
            key={day}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              height: 92,
              borderRadius: radii.card,
              background: colors.blanco,
              padding: "0 20px",
              marginBottom: 12,
              fontFamily: fonts.ui,
              fontWeight: 700,
              fontSize: 30,
            }}
          >
            <span>{day}</span>
            {isClosed ? (
              <Pill size={26} bg={closed > 0.5 ? colors.tomate : colors.gris} color={closed > 0.5 ? colors.blanco : colors.negro}>
                {closed > 0.5 ? d.cerrado : d.rango}
              </Pill>
            ) : (
              <Pill size={26} bg={colors.gris} color={colors.negro}>
                {d.rango}
              </Pill>
            )}
          </div>
        );
      })}
    </>
  );
};

const Planificador: React.FC<{ d: D["planificador"] }> = ({ d }) => {
  const tones = [colors.amarillo, colors.rosa, colors.verde];
  return (
    <>
      <Title>{d.encabezado}</Title>
      {d.contadores.map((c, i) => (
        <div
          key={c.etiqueta}
          style={{
            borderRadius: radii.card,
            background: tones[i % tones.length],
            padding: "22px 24px",
            marginBottom: 14,
          }}
        >
          <div style={{ fontFamily: fonts.ui, fontWeight: 700, fontSize: 26 }}>{c.etiqueta}</div>
          <Counter
            to={c.valor}
            start={26 + i * 8}
            duration={28}
            style={{ fontFamily: fonts.display, fontWeight: 800, fontSize: 96, lineHeight: 1, letterSpacing: "-0.05em" }}
          />
        </div>
      ))}
    </>
  );
};

export const Admin: React.FC<{ props: MesaProps }> = ({ props }) => {
  const { vertical } = useLayout();
  const d = props.admin;
  const s = vertical ? 0.7 : 0.62;
  const dx = vertical ? 335 : 275;
  const dy = vertical ? 80 : 60;
  const phones = [
    { x: -dx, y: -dy, node: <Productos d={d.productos} />, delay: 8, tilt: { x: 4, y: 10 } },
    { x: 0, y: 0, node: <Horarios d={d.horarios} />, delay: 16, tilt: { x: 4, y: 0 } },
    { x: dx, y: dy, node: <Planificador d={d.planificador} />, delay: 24, tilt: { x: 4, y: -10 } },
  ];
  return (
    <SceneLayout
      bg={colors.blanco}
      text={<Headline lines={d.lineas} size={vertical ? 230 : 230} color={colors.negro} />}
      visual={
        <div style={{ position: "relative", width: 0, height: 0 }}>
          {phones.map((ph, i) => (
            <div
              key={i}
              style={{
                position: "absolute",
                left: ph.x - (440 * s) / 2,
                top: ph.y - (900 * s) / 2,
              }}
            >
              <PhoneFrame
                variant="light"
                scale={s}
                tilt={ph.tilt}
                delay={ph.delay}
                floatAmp={10}
                phase={i * 1.3}
                floatPeriod={3.4 + i * 0.3}
              >
                {ph.node}
              </PhoneFrame>
            </div>
          ))}
        </div>
      }
    />
  );
};
