import React from "react";
import { colors } from "../theme";

type IllustrationProps = { size?: number; color?: string; accent?: string };

const Svg: React.FC<{ size: number; children: React.ReactNode }> = ({
  size,
  children,
}) => (
  <svg width={size} height={size} viewBox="0 0 100 100" style={{ display: "block" }}>
    {children}
  </svg>
);

export const Cup: React.FC<IllustrationProps> = ({
  size = 100,
  color = colors.crema,
  accent = colors.negro,
}) => (
  <Svg size={size}>
    <path d="M70 38h6a10 10 0 0 1 0 22h-6" stroke={color} strokeWidth="7" fill="none" strokeLinecap="round" />
    <path d="M16 30h56v28a22 22 0 0 1-22 22h-12a22 22 0 0 1-22-22z" fill={color} />
    <rect x="16" y="44" width="56" height="8" fill={accent} opacity="0.18" />
    <rect x="8" y="84" width="72" height="7" rx="3.5" fill={accent} />
    <path d="M34 8c-5 6 5 8 0 15M50 8c-5 6 5 8 0 15" stroke={accent} strokeWidth="4" fill="none" strokeLinecap="round" />
  </Svg>
);

export const Bag: React.FC<IllustrationProps> = ({
  size = 100,
  color = colors.crema,
  accent = colors.negro,
}) => (
  <Svg size={size}>
    <path d="M36 34v-8a14 14 0 0 1 28 0v8" stroke={accent} strokeWidth="5" fill="none" strokeLinecap="round" />
    <rect x="18" y="32" width="64" height="58" rx="9" fill={color} />
    <rect x="18" y="32" width="64" height="14" rx="7" fill={accent} opacity="0.18" />
    <circle cx="50" cy="66" r="9" fill={accent} />
  </Svg>
);

export const Cookie: React.FC<IllustrationProps> = ({
  size = 100,
  color = colors.crema,
  accent = colors.negro,
}) => (
  <Svg size={size}>
    <circle cx="50" cy="50" r="40" fill={color} />
    <circle cx="36" cy="38" r="6" fill={accent} />
    <circle cx="62" cy="34" r="5" fill={accent} />
    <circle cx="58" cy="60" r="7" fill={accent} />
    <circle cx="34" cy="62" r="5" fill={accent} />
  </Svg>
);

export const Ticket: React.FC<IllustrationProps> = ({
  size = 100,
  color = colors.crema,
  accent = colors.negro,
}) => (
  <Svg size={size}>
    <path d="M8 24h84v20a7 7 0 0 0 0 14v18H8V58a7 7 0 0 0 0-14z" fill={color} />
    <path d="M32 24v52" stroke={accent} strokeWidth="3" strokeDasharray="5 5" opacity="0.5" />
    <rect x="44" y="38" width="36" height="7" rx="3.5" fill={accent} />
    <rect x="44" y="54" width="24" height="7" rx="3.5" fill={accent} opacity="0.5" />
  </Svg>
);

export const ICONS = { taza: Cup, bolsa: Bag, galleta: Cookie, ticket: Ticket };
export type IconName = keyof typeof ICONS;

// Check mark that draws itself; `progress` in [0, 1].
export const Check: React.FC<{ size?: number; progress: number; color?: string; bg?: string }> = ({
  size = 120,
  progress,
  color = colors.negro,
  bg = colors.verde,
}) => (
  <svg width={size} height={size} viewBox="0 0 100 100" style={{ display: "block" }}>
    <circle cx="50" cy="50" r="46" fill={bg} />
    <path
      d="M27 52l16 16 31-34"
      stroke={color}
      strokeWidth="10"
      fill="none"
      strokeLinecap="round"
      strokeLinejoin="round"
      pathLength={1}
      strokeDasharray={1}
      strokeDashoffset={1 - progress}
    />
  </svg>
);

// Decorative QR-like grid (not scannable, on purpose).
export const QR: React.FC<{ size?: number; color?: string }> = ({
  size = 130,
  color = colors.negro,
}) => {
  const n = 11;
  const cells: React.ReactNode[] = [];
  const finder = (i: number, j: number) =>
    (i < 3 && j < 3) || (i < 3 && j >= n - 3) || (i >= n - 3 && j < 3);
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      if (finder(i, j)) continue;
      if ((i * 7 + j * 13 + i * j) % 3 === 0) {
        cells.push(<rect key={`${i}-${j}`} x={j} y={i} width="1" height="1" fill={color} />);
      }
    }
  }
  const corner = (x: number, y: number) => (
    <g key={`${x}-${y}`}>
      <rect x={x} y={y} width="3" height="3" fill={color} />
      <rect x={x + 0.7} y={y + 0.7} width="1.6" height="1.6" fill={colors.blanco} />
      <rect x={x + 1} y={y + 1} width="1" height="1" fill={color} />
    </g>
  );
  return (
    <svg width={size} height={size} viewBox={`0 0 ${n} ${n}`} style={{ display: "block" }}>
      {cells}
      {corner(0, 0)}
      {corner(n - 3, 0)}
      {corner(0, n - 3)}
    </svg>
  );
};

export const Eye: React.FC<{ size?: number; color?: string; off?: boolean }> = ({
  size = 40,
  color = colors.negro,
  off = false,
}) => (
  <svg width={size} height={size} viewBox="0 0 100 100" style={{ display: "block" }}>
    <path d="M8 50c14-24 70-24 84 0-14 24-70 24-84 0z" fill="none" stroke={color} strokeWidth="8" />
    <circle cx="50" cy="50" r="12" fill={color} />
    {off ? <path d="M16 86L84 14" stroke={color} strokeWidth="9" strokeLinecap="round" /> : null}
  </svg>
);

export const Pencil: React.FC<{ size?: number; color?: string }> = ({
  size = 40,
  color = colors.negro,
}) => (
  <svg width={size} height={size} viewBox="0 0 100 100" style={{ display: "block" }}>
    <path d="M18 82l6-22 40-40 16 16-40 40z" fill={color} />
  </svg>
);
