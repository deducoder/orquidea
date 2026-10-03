import { Easing } from "remotion";
import { loadFont as loadDisplay } from "@remotion/google-fonts/Outfit";
import { loadFont as loadUi } from "@remotion/google-fonts/DMSans";

// Provisional palette: Mesa has no brand yet. Change values here only.
export const colors = {
  tomate: "#E8432E",
  rosa: "#FFC4D4",
  cobalto: "#1C4DE0",
  negro: "#0A0A0B",
  crema: "#FFF3DF",
  blanco: "#FFFFFF",
  verde: "#19D66B",
  amarillo: "#FFD43B",
  // UI neutrals used inside the phones
  gris: "#ECE7DE",
  grisOscuro: "#1C1C1F",
  grisMedio: "#8A857C",
} as const;

export type ColorName = keyof typeof colors;

const display = loadDisplay("normal", {
  weights: ["600", "800"],
  subsets: ["latin"],
});
const ui = loadUi("normal", { weights: ["500", "700"], subsets: ["latin"] });

export const fonts = {
  display: display.fontFamily,
  ui: ui.fontFamily,
};

export const radii = {
  pill: 999,
  card: 28,
  chip: 22,
  phone: 64,
  screen: 52,
};

export const easing = {
  out: Easing.bezier(0.16, 1, 0.3, 1),
  inOut: Easing.bezier(0.65, 0, 0.35, 1),
};

export const springs = {
  snappy: { damping: 14, stiffness: 200, mass: 0.6 },
  soft: { damping: 18, stiffness: 120, mass: 0.8 },
};
