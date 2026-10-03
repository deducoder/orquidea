# Mesa — motion graphic de presentación

Video de presentación de Mesa (preorden y prepago para una cafetería
autoservicio universitaria), hecho con Remotion 4.0.532.

| Composición | Formato | Duración |
|---|---|---|
| `MesaVertical` | 1080x1920, 30 fps | 38 s (1140 frames) |
| `MesaHorizontal` | 1920x1080, 30 fps | 38 s (1140 frames) |

Las dos usan las mismas escenas; el layout se adapta con `useLayout()` y
`SceneLayout` (`src/Mesa/layout.tsx`).

## Comandos

```console
npm i
npm run dev                # Remotion Studio
npm run render:vertical    # out/mesa-vertical.mp4 (h264)
npm run render:horizontal  # out/mesa-horizontal.mp4 (h264)
npm run lint               # eslint + tsc
npx remotion still MesaVertical out/still.png --frame=300
```

Las fuentes (Outfit y DM Sans) se descargan de Google Fonts en cada render,
así que el render necesita red.

## Qué editar

- **Textos y cifras:** `src/Mesa/data.ts` (`defaultProps`). Los props están
  tipados con zod y se editan en el panel de Props de Remotion Studio.
- **Colores, tipografías, radios, easing y springs:** `src/Mesa/theme.ts`.
  La paleta es provisional (Mesa aún no tiene marca).
- **Duración de cada escena y tipo de transición:** el arreglo `SCENES` en
  `src/Mesa/Mesa.tsx`. `seconds` es el tiempo visible de la escena y `into`
  es la transición hacia la siguiente (`cut`, `wipe` o `slide`). La duración
  total se recalcula sola (`MESA_TOTAL_FRAMES`). Ritmo general (frames por
  entrada, escalonado, solape de transición) en `src/Mesa/anim.ts`.
- **Logo:** prop opcional `logo` (ruta de `staticFile` o URL). Si está vacío
  se usa el wordmark de texto.
- **Audio:** sin audio por ahora. Para agregar una pista, pon el archivo en
  `public/` y llena el prop `audioSrc` (por ejemplo `"/mesa.mp3"`) en
  Studio o en `defaultProps`; `Mesa.tsx` lo monta con `Html5Audio`.

## Estructura

```
src/Mesa/
  theme.ts  data.ts  anim.ts  layout.tsx  Mesa.tsx
  components/  Headline  PhoneFrame  Pill  Chip  Counter
               Illustrations  Wordmark
  scenes/      una escena por archivo, en orden del guion
```
