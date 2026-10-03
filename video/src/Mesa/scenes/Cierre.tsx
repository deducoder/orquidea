import React from "react";
import { Headline } from "../components/Headline";
import { Wordmark } from "../components/Wordmark";
import { SceneLayout, useLayout } from "../layout";
import { useEnter } from "../anim";
import type { MesaProps } from "../data";
import { colors, fonts } from "../theme";

export const Cierre: React.FC<{ props: MesaProps }> = ({ props }) => {
  const { vertical } = useLayout();
  const d = props.cierre;
  const mark = useEnter(0);
  const contact = useEnter(32);
  return (
    <SceneLayout
      bg={colors.tomate}
      text={
        <>
          <div style={{ transform: `translateY(${(1 - mark) * -200}px)`, opacity: Math.min(1, mark * 3), marginBottom: 56 }}>
            <Wordmark brand={props.marca} logo={props.logo} size={110} color={colors.crema} />
          </div>
          <Headline
            lines={d.lineas.map((text, i) => ({ text, color: i === 0 ? colors.crema : colors.negro }))}
            size={vertical ? 170 : 190}
            delay={8}
          />
          <div
            style={{
              marginTop: 60,
              fontFamily: fonts.ui,
              fontWeight: 700,
              fontSize: 44,
              color: colors.crema,
              opacity: contact,
              transform: `translateY(${(1 - contact) * 40}px)`,
            }}
          >
            {d.contacto}
          </div>
        </>
      }
    />
  );
};
