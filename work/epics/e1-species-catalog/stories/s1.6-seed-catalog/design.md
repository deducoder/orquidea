# Story s1.6: Seed catalog — Design

> Complexity: simple

## 1 · What & why

**Problem:** el catálogo real está vacío: la aplicación arranca y no muestra ninguna especie, y la métrica líder de la épica pide ver una especie real en su ficha.
**Value:** 100 especies nativas de Chiapas con cuidados y fuente, listas para consultar y para medir `must-perf-001` sobre datos reales.

## 2 · Approach

La investigación (`work/research/chiapas-orchid-seed/report.md`) produjo la lista y las fuentes; esta historia solo materializa el resultado: un archivo JSON por especie en `src/orquidea/datos/catalogo/` y pruebas que fijan que el catálogo real carga y cumple un mínimo de calidad. No hay código de aplicación nuevo.

**Components affected:**

- `src/orquidea/datos/catalogo/*.json`: create — 100 archivos generados con el esquema de s1.2, uno por especie; el `.gitkeep` se elimina.
- `tests/test_catalogo_real.py`: create — el catálogo real carga y sus fuentes son verificables.

**Legacy sweep:** nada — net-new (se retira el `.gitkeep`, que solo mantenía vacío el directorio).

Gemba: `cargar_catalogo`, `Especie` (s1.2) y las rutas (s1.3, s1.4) se reutilizan sin cambios; el directorio real ya es el que `app.py` carga al arrancar. Gobernanza: RF-01, RF-03, `must-data-001` (fuente por especie y por cuidado, garantizada por el esquema y por las pruebas), `must-perf-001` (se mide en `epic-review`; las 100 fichas son texto plano). Hallazgo de la investigación que la historia hereda: los cuidados son del género, no de la especie, y cada dato lo declara en su fuente; es un límite de honestidad que el humano debe conocer y no un defecto por corregir aquí.

## 3 · Interface / examples

### Usage (API / CLI)

```python
from orquidea.datos.catalogo import DIRECTORIO_CATALOGO, cargar_catalogo

especies = cargar_catalogo(DIRECTORIO_CATALOGO)
```

### Expected output (success + error)

```
len(especies) >= 100, sin CatalogoInvalido
especies[0].id == "arpophyllum-giganteum"          (orden por id)
cada cuidado.fuente y cada fuentes[i] contienen una URL https:// y "consultada el"
GET /especies -> 200, 100 enlaces a /especies/{id}
GET /especies/epidendrum-radicans -> 200, luz/riego/temperatura/sustrato con "AOS, Reedstem Epidendrum Culture"
```

### Key data structures (if applicable)

Sin estructuras nuevas: el `Especie` de s1.2.

## 4 · Acceptance criteria

- **Must:** el catálogo real carga con 100 especies sin errores; cada fuente (de especie y de cuidado) trae una URL y la fecha de consulta; ninguna especie repetida; `./scripts/check` en verde.
- **Should:** la lista y una ficha real responden 200 vía la aplicación con el catálogo real.
- **Must NOT:** presentar cuidados de género como medidos para la especie sin decirlo; inventar un dato sin fuente; copiar texto literal de las fuentes (se parafrasea).

### Deduced criteria

- Cuidado de género declarado como tal: confirmed — la fuente de cada cuidado y la descripción lo dicen; una prueba lo fija.
- must-perf-001 sobre el catálogo real: confirmed — se mide en `epic-review` (manual, con "Slow 3G"); aquí se verifica el peso de las páginas en la prueba manual.

### Scenarios (delta over the scope)

```gherkin
Given el catálogo real
When abro la ficha de una especie que usa la hoja de otro género
Then su fuente dice cuál (por ejemplo Guarianthe con la hoja de Cattleya)
```
