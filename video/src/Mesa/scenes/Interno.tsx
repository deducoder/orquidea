import React from "react";
import { useCurrentFrame } from "remotion";
import { Chip } from "../components/Chip";
import { Headline } from "../components/Headline";
import { SceneLayout, useLayout } from "../layout";
import { ramp } from "../anim";
import type { MesaProps } from "../data";
import { colors, fonts } from "../theme";

type D = MesaProps["interno"];

const Node: React.FC<{
  cx: number;
  cy: number;
  w: number;
  h: number;
  bg: string;
  color: string;
  at: number;
  title: string[];
  sub?: string;
  size: number;
}> = ({ cx, cy, w, h, bg, color, at, title, sub, size }) => {
  const frame = useCurrentFrame();
  const p = ramp(frame, at, at + 12);
  return (
    <g transform={`translate(${cx} ${cy}) scale(${p})`} opacity={Math.min(1, p * 3)}>
      <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={34} fill={bg} />
      {title.map((t, i) => (
        <text
          key={t}
          x={0}
          y={(i - (title.length - 1) / 2) * size * 0.95 + size * 0.34 - (sub ? size * 0.28 : 0)}
          textAnchor="middle"
          fontFamily={fonts.display}
          fontWeight={800}
          fontSize={size}
          fill={color}
          letterSpacing={-1.5}
        >
          {t}
        </text>
      ))}
      {sub ? (
        <text x={0} y={size * 0.9} textAnchor="middle" fontFamily={fonts.ui} fontWeight={700} fontSize={30} fill={color} opacity={0.7}>
          {sub}
        </text>
      ) : null}
    </g>
  );
};

const Link: React.FC<{ d: string; at: number; head: string }> = ({ d, at, head }) => {
  const frame = useCurrentFrame();
  const p = ramp(frame, at, at + 14);
  return (
    <g>
      <path
        d={d}
        pathLength={1}
        strokeDasharray={1}
        strokeDashoffset={1 - p}
        stroke={colors.crema}
        strokeWidth={7}
        fill="none"
        strokeLinecap="round"
      />
      <path d={head} fill={colors.crema} opacity={p > 0.95 ? 1 : 0} />
    </g>
  );
};

const Diagram: React.FC<{ d: D }> = ({ d }) => (
  <svg viewBox="0 0 1000 720" style={{ width: "100%", height: "auto", display: "block" }}>
    <Node cx={130} cy={220} w={220} h={130} bg={colors.crema} color={colors.negro} at={4} title={[d.cliente]} size={44} />
    <Node cx={500} cy={220} w={250} h={190} bg={colors.amarillo} color={colors.negro} at={14} title={[d.mesa]} sub={d.mesaSub} size={72} />
    <Node cx={870} cy={220} w={220} h={150} bg={colors.cobalto} color={colors.blanco} at={24} title={d.pago} size={42} />
    <Node cx={500} cy={580} w={320} h={150} bg={colors.rosa} color={colors.negro} at={44} title={[d.personal]} sub={d.personalSub} size={50} />
    {/* Cliente -> Mesa */}
    <Link at={10} d="M244 220 H360" head="M372 220 l-24 -14 v28z" />
    {/* Mesa <-> Pago */}
    <Link at={30} d="M632 190 H746" head="M758 190 l-24 -14 v28z" />
    <Link at={34} d="M746 252 H632" head="M620 252 l24 -14 v28z" />
    {/* Mesa -> Personal */}
    <Link at={50} d="M500 322 V494" head="M500 506 l-14 -24 h28z" />
  </svg>
);

export const Interno: React.FC<{ props: MesaProps }> = ({ props }) => {
  const { vertical } = useLayout();
  const d = props.interno;
  return (
    <SceneLayout
      bg={colors.negro}
      text={
        <div style={{ position: "relative" }}>
          <div style={{ position: "relative", height: 70, marginBottom: 20 }}>
            <Chip bg={colors.tomate} color={colors.crema} size={36} rotate={-3} style={{ left: 0, top: 0 }}>
              {d.etiqueta}
            </Chip>
          </div>
          <Headline lines={d.lineas} size={vertical ? 118 : 110} color={colors.blanco} maxWidth={vertical ? 940 : 760} delay={56} />
        </div>
      }
      visual={<div style={{ width: "100%" }}>{<Diagram d={d} />}</div>}
    />
  );
};
