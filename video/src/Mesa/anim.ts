import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { easing, springs } from "./theme";

export const FPS = 30;
// Wipe/slide overlap between scenes, in frames (6 to 8 per the brief).
export const TRANSITION_FRAMES = 7;
// Every element enters in at most this many frames.
export const ENTER_FRAMES = 14;
export const STAGGER = 5;

export const useEnter = (
  delay = 0,
  duration = ENTER_FRAMES,
  config: typeof springs.snappy = springs.snappy,
) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame, fps, delay, durationInFrames: duration, config });
};

// Sine in [-1, 1] with the given period, for idle float/wobble loops.
export const useLoop = (periodSeconds: number, phase = 0) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return Math.sin(
    (frame / fps) * ((Math.PI * 2) / periodSeconds) + phase,
  );
};

export const ramp = (
  frame: number,
  from: number,
  to: number,
  a = 0,
  b = 1,
  ease: (t: number) => number = easing.out,
) =>
  interpolate(frame, [from, to], [a, b], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });

// 1 -> 1 + amp -> 1 around `at`, for button presses and badges.
export const pulse = (frame: number, at: number, amp = 0.12, dur = 10) =>
  interpolate(frame, [at, at + dur * 0.4, at + dur], [1, 1 + amp, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
