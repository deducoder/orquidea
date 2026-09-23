# Story s1: Adopt the gemba-design 0.23.0 vocabulary — Scope

## User story

Como dueño de Orquídea,
quiero que la identidad se declare con lo que el formato de gemba-design 0.23.0 ya expresa (radio, color de borde, mínimo de control y tokens en español) y cerrar lo que e5 dejó abierto en la interfaz vestida,
para que `DESIGN.md` diga en tokens lo que hoy solo dicen ADR-014 y ADR-015, y la interfaz no tenga juicios sin firmar ni ajustes sin decidir.

## Acceptance criteria

```gherkin
@stated
Given ningún valor nuevo de la identidad producido todavía
When se abre el ADR de esta historia en `proposed`
Then trae los criterios de fitness de lo nuevo, con su estrato, aprobados por el humano y commiteados antes del primer valor producido

@stated
Given `governance/identity/ui/DESIGN.md` generado con `design-md.py` de gemba-design 0.23.0
When se lee su frontmatter
Then las esquinas son un token de `rounded`, los componentes con borde lo citan con `borderColor`, los controles declaran su mínimo con `minWidth`, y los roles llevan los nombres en español con acentos

@stated
Given el comando de generación registrado en el ADR
When se corre dos veces sobre las tablas de `governance/identity/ui/`
Then sale idéntico al `DESIGN.md` del repositorio

@deduced
Given los tokens renombrados
When corre `./scripts/check`
Then la prueba de tokens de la hoja, la de objetivos y la de piso siguen verdes con los nombres nuevos, y ninguna propiedad de `identidad.css` usa un nombre anterior

@stated
Given la interfaz a 360 px
When el humano la recorre
Then el criterio 3 de ADR-009 (la foto es la protagonista) y el subtítulo frente al cuerpo (ADR-015, decisión 5) quedan firmados o rechazados con nombre y fecha

@stated
Given un enlace con `accion` y el formulario de Acceso
When se decide cada ajuste
Then la sangría de 8 px de los enlaces `accion` y el botón "Entrar" pegado al campo quedan corregidos o dejados como están, con la decisión escrita
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `semantics.md` con `accion-fondo` y `linea` | se renombra y se regenera `DESIGN.md` | `colors: acción-fondo: "#1F3A5F"`, `línea: "#8C8475"`; en la hoja, `var(--colors-acción-fondo)` |
| ADR-015, decisión 3 (esquinas rectas, sin token) | se declara el radio | `rounded: none: "0px"` en `DESIGN.md`, y `campo` con `rounded: "{rounded.none}"` |
| `enlace-navegacion` con `width: {spacing.step-6}` usado como mínimo | se declara el mínimo | `minWidth: "{spacing.step-6}"` |

## In scope

- Radio declarado como token (`Level | Value`) y citado por los componentes que lo usan.
- `borderColor` en los componentes con borde (campo, y los que el diseño encuentre), en lugar del `--gap` de ADR-014.
- `minWidth` / `minHeight` como mínimo de control declarado.
- Renombre de los tokens a español con acentos (`línea`, `acción-*`), en `semantics.md`, `DESIGN.md`, `identidad.css` y las pruebas. ADR nuevo que sustituye la decisión 6 de ADR-014.
- Regenerar `DESIGN.md` con el generador de 0.23.0 (trae los dos Known Gaps nuevos).
- Los criterios de fitness de lo nuevo, propuestos por el agente y aprobados por el humano antes de producir.
- Del parking lot de e5 (entrada "La interfaz vestida de e5…"):
  - la sangría de 8 px de los enlaces `accion`;
  - el botón "Entrar" pegado al campo en Acceso;
  - la firma o el rechazo del criterio 3 de ADR-009 (la foto como protagonista);
  - la firma o el rechazo del subtítulo frente al cuerpo (ADR-015, decisión 5).
- **Recalcular la cadena con 0.23.0 y corregir lo que cambie.** Se vuelven a correr las derivaciones (`derivar-primitivas.py`, `derivar-medidas.py`) y las mediciones (`tokens.py pairs`, `targets`, `provenance`, `contraste-de-lectura.py`, `comprobar-medidas.py`) sobre lo declarado de nuevo. Si una cifra cambia o aparece información nueva (niveles de `rounded`, pares de componente que salen de `borderColor`, objetivos que salen del mínimo declarado), se corrige en su eslabón y se propaga hasta la hoja.
- Trazo, elevación, medida de texto e iconografía: se declaran donde 0.23.0 lo permita; donde no, quedan como `--gap` con la decisión escrita en el ADR (ninguna sombra, ningún ícono, trazos de ADR-015) y la razón de por qué el formato no los lleva.
- `survival-review` sobre las piezas tocadas.
- Retirar del parking lot la entrada de las referencias ASCII (0.23.0 la corrige) y la de la interfaz vestida, con lo que citaba cada una.

## Out of scope

- Copiar o parchar un instrumento del addon para que exprese lo que 0.23.0 no expresa (`{stroke.*}` sale `refused`; elevación "not derived"; iconografía en Known Gaps; `targets` no lee `minWidth`): el addon prohíbe una segunda copia. Lo que falte va al parking lot como hallazgo del addon.
- La columna `Variant` con `—` que `invariance.py` no lee: sigue sin corregir en 0.23.0; la entrada del parking lot se queda.
- Que `precedence.py` no pueda leer el `DESIGN.md` generado (sin `decision:` en el frontmatter): hallazgo del addon, al parking lot, no se rodea aquí.
- La medición con "Slow 3G": ligada al primer despliegue (parking lot).
- Quitar `'unsafe-inline'` de la CSP: su propia historia.

## Done when

- [stated] El ADR de esta historia estaba commiteado en `proposed`, con los criterios de fitness aprobados, antes del primer commit que produce un valor, y `precedence.py` lo confirma en las piezas que lo citan.
- [stated] `DESIGN.md` declara el radio, `borderColor` y `minWidth`, y los roles en español; regenerado con 0.23.0, sale idéntico dos veces.
- [stated] La cadena se recalculó con 0.23.0 y cada cifra que cambió está corregida en su eslabón y en la hoja; si no cambió ninguna, se dice con la salida de cada comando.
- [deduced] `./scripts/check` verde con los nombres nuevos, y ningún nombre ASCII anterior en `identidad.css` ni en las tablas.
- [stated] Los dos juicios tienen firma o rechazo con nombre y fecha; los dos ajustes, una decisión escrita.
- [deduced] `survival-review` corrido sobre las piezas tocadas, con su población contada.
- [deduced] Las dos entradas retiradas del parking lot, y el hallazgo de `precedence.py` aparcado.

## Notes

- Standalone: e5 está cerrada. Sale por su cuenta con `integrate` al cerrar.
- Base: la survival-review con 0.23.0 de la sesión del 2026-09-23 (sondas en el scratchpad: acentos exit 0; `borderColor`, `rounded.none` y `minWidth` aceptados; `{stroke.fino}` rechazado).
- Los dos juicios requieren que el humano recorra la interfaz a 360 px; es el momento que fijaba la promoción de la entrada del parking lot.
- El parking lot pedía que un ajuste decidido fuera "arreglo propio contra ADR-015"; el humano lo junta en esta historia.
