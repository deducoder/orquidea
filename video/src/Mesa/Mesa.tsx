import React from "react";
import { Html5Audio } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { FPS, TRANSITION_FRAMES } from "./anim";
import type { MesaProps } from "./data";
import { Admin } from "./scenes/Admin";
import { Aviso } from "./scenes/Aviso";
import { Carta } from "./scenes/Carta";
import { Cierre } from "./scenes/Cierre";
import { Cocina } from "./scenes/Cocina";
import { Interno } from "./scenes/Interno";
import { Pago } from "./scenes/Pago";
import { Presentacion } from "./scenes/Presentacion";
import { Problema } from "./scenes/Problema";
import { Whatsapp } from "./scenes/Whatsapp";

type Cut = "cut" | "wipe" | "slide";

// Edit durations (seconds on screen) and the transition INTO the next scene.
const SCENES: {
  id: string;
  seconds: number;
  into: Cut;
  Scene: React.FC<{ props: MesaProps }>;
}[] = [
  { id: "problema", seconds: 4, into: "cut", Scene: Problema },
  { id: "presentacion", seconds: 3, into: "wipe", Scene: Presentacion },
  { id: "carta", seconds: 5, into: "slide", Scene: Carta },
  { id: "pago", seconds: 4, into: "wipe", Scene: Pago },
  { id: "whatsapp", seconds: 4, into: "cut", Scene: Whatsapp },
  { id: "cocina", seconds: 5, into: "wipe", Scene: Cocina },
  { id: "aviso", seconds: 3, into: "slide", Scene: Aviso },
  { id: "admin", seconds: 4, into: "wipe", Scene: Admin },
  { id: "interno", seconds: 3, into: "cut", Scene: Interno },
  { id: "cierre", seconds: 3, into: "cut", Scene: Cierre },
];

// Each scene also holds the overlap of the transition that follows it, so
// the visible time per scene equals `seconds` and the total is their sum.
const sceneFrames = (i: number) =>
  SCENES[i].seconds * FPS + (i < SCENES.length - 1 && SCENES[i].into !== "cut" ? TRANSITION_FRAMES : 0);

export const MESA_TOTAL_FRAMES = SCENES.reduce((a, s) => a + s.seconds * FPS, 0);

const timing = linearTiming({ durationInFrames: TRANSITION_FRAMES });

const transition = (kind: Cut, i: number, key: string) =>
  kind === "slide" ? (
    <TransitionSeries.Transition
      key={key}
      presentation={slide({ direction: i % 2 === 0 ? "from-bottom" : "from-right" })}
      timing={timing}
    />
  ) : (
    <TransitionSeries.Transition
      key={key}
      presentation={wipe({ direction: i % 2 === 0 ? "from-left" : "from-top" })}
      timing={timing}
    />
  );

export const Mesa: React.FC<MesaProps> = (props) => {
  const children: React.ReactElement[] = [];
  SCENES.forEach(({ id, into, Scene }, i) => {
    children.push(
      <TransitionSeries.Sequence key={id} durationInFrames={sceneFrames(i)}>
        <Scene props={props} />
      </TransitionSeries.Sequence>,
    );
    if (i < SCENES.length - 1 && into !== "cut") {
      children.push(
        transition(into, i, `${id}-t`),
      );
    }
  });
  return (
    <>
      <TransitionSeries>{children}</TransitionSeries>
      {/* Audio slot: set the `audioSrc` prop (e.g. staticFile("mesa.mp3")). */}
      {props.audioSrc ? <Html5Audio src={props.audioSrc} /> : null}
    </>
  );
};
