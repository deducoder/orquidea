import "./index.css";
import React from "react";
import { Composition } from "remotion";
import { FPS } from "./Mesa/anim";
import { defaultProps, mesaSchema } from "./Mesa/data";
import { MESA_TOTAL_FRAMES, Mesa } from "./Mesa/Mesa";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MesaVertical"
        component={Mesa}
        durationInFrames={MESA_TOTAL_FRAMES}
        fps={FPS}
        width={1080}
        height={1920}
        schema={mesaSchema}
        defaultProps={defaultProps}
      />
      <Composition
        id="MesaHorizontal"
        component={Mesa}
        durationInFrames={MESA_TOTAL_FRAMES}
        fps={FPS}
        width={1920}
        height={1080}
        schema={mesaSchema}
        defaultProps={defaultProps}
      />
    </>
  );
};
