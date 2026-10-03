import React from "react";
import { Headline } from "../components/Headline";
import { Bag, Cup, Ticket } from "../components/Illustrations";
import { SceneLayout, useLayout } from "../layout";
import { useEnter, useLoop } from "../anim";
import type { MesaProps } from "../data";
import { colors } from "../theme";

const Floating: React.FC<{
  delay: number;
  rotate: number;
  phase: number;
  style: React.CSSProperties;
  children: React.ReactNode;
}> = ({ delay, rotate, phase, style, children }) => {
  const p = useEnter(delay);
  const loop = useLoop(3, phase);
  return (
    <div
      style={{
        position: "absolute",
        transform: `translateY(${loop * 12}px) rotate(${rotate + loop * 4}deg) scale(${p})`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

export const Presentacion: React.FC<{ props: MesaProps }> = ({ props }) => {
  const { vertical } = useLayout();
  const { titulo, lineas } = props.presentacion;
  const colorsByLine = [colors.crema, colors.negro, colors.amarillo];
  return (
    <SceneLayout
      bg={colors.tomate}
      text={
        <>
          <Headline lines={[{ text: titulo, offset: -6 }]} size={vertical ? 400 : 380} color={colors.crema} />
          <div style={{ height: vertical ? 40 : 20 }} />
          <Headline
            lines={lineas.map((text, i) => ({ text, color: colorsByLine[i % 3] }))}
            size={vertical ? 170 : 150}
            delay={18}
          />
        </>
      }
      visual={
        <div style={{ position: "relative", width: vertical ? 700 : 520, height: vertical ? 500 : 700 }}>
          <Floating delay={30} rotate={-10} phase={0} style={{ left: 20, top: 20 }}>
            <Cup size={220} color={colors.crema} accent={colors.negro} />
          </Floating>
          <Floating delay={36} rotate={8} phase={1.4} style={{ left: vertical ? 330 : 240, top: vertical ? 160 : 230 }}>
            <Ticket size={240} color={colors.amarillo} accent={colors.negro} />
          </Floating>
          <Floating delay={42} rotate={-6} phase={2.6} style={{ left: vertical ? 90 : 20, top: vertical ? 300 : 460 }}>
            <Bag size={220} color={colors.rosa} accent={colors.negro} />
          </Floating>
        </div>
      }
    />
  );
};
