# Research: Especies semilla del catálogo de Chiapas

## Pregunta y decisión que informa

**Pregunta primaria (falsable):** ¿es posible reunir 100 orquídeas nativas de Chiapas, entre las más conocidas y populares, con datos de luz, riego, temperatura y sustrato respaldados por una fuente real consultada para cada dato (`must-data-001`)?
**Informa:** s1.6 (conjunto semilla) y, con ello, la métrica líder del brief. Profundidad: estándar. Respuesta del humano al stop P5: "Debemos hacer un research para buscar los datos... Pongamos las 100 más conocidas y populares".

## Recomendación

Sí es posible, con una limitación que el humano debe conocer: **los cuidados son del género, no de la especie.** Para las 100 especies existe fuente citable de cuidados solo a nivel de género (AOS). Ninguna fuente consultada da cuidados medidos para cada una de esas especies de Chiapas. Cada dato lo dice en su propia fuente ("cuidado del género, no específico de la especie") y la descripción de la ficha lo repite. Confianza: **MEDIA** en que los cuidados sean una guía razonable; **BAJA** en que sean exactos para cada especie.

## Método

1. **Universo y popularidad.** Observaciones de grado de investigación de Orchidaceae en Chiapas (iNaturalist, lugar 97003, `quality_grade=research`, `native=true`, `captive=false`, consulta del 2026-09-19): 444 especies, 440 nativas. "Más conocidas y populares" se operacionaliza como **más observadas por la comunidad en el estado** (medida objetiva y reproducible). Es una proxy: favorece plantas visibles y de camino, y no mide el comercio de plantas ni su cultivo.
2. **Nativas.** Se usó el filtro `native=true` de iNaturalist (listas de establecimiento por lugar). Se intentó verificar con Kew POWO, pero su API está detrás de un desafío anti-bots de Cloudflare y no se eludió. Queda sin doble verificación.
3. **Cuidados.** Para cada género, la "Care and Culture Card" de su página en la AOS (`https://www.aos.org/explore/{género}`) y, donde no hay tarjeta útil, la hoja de cultivo de la AOS: Oncidium (para Oncidium y Trichocentrum), Cattleya (para Guarianthe), Gongora, Catasetum, y para *Epidendrum radicans* el artículo de la AOS sobre Epidendrum de tallo de caña. Los textos son paráfrasis en español; ninguna cita literal.
4. **Regla de selección.** Se recorrió la lista por número de observaciones y se tomaron las primeras 100 cuyo género tiene una fuente de cuidados utilizable.

## Hallazgos y confianza

- **H1 — Hay al menos 440 orquídeas nativas de Chiapas con observaciones de grado de investigación.** Confianza MEDIA: una plataforma con dos filtros propios (nativa, no cautiva) y sin doble verificación; es coherente con los 325 taxa de una sola región del estado (fuente 3) y con los ~700 que se reportan para todo el estado (fuente 4, solo referida).
- **H2 — Los cuidados por género están documentados por la AOS de forma consistente** (luz, temperatura, riego, sustrato). Confianza MEDIA: una sola organización, aunque de referencia; las tarjetas de género y las hojas de cultivo de la misma AOS coinciden en dirección (luz brillante, temperaturas intermedias, riego regular).
- **H3 — La AOS advierte que su hoja de Cattleya "puede no ser representativa de todas las plantas de la alianza o del género".** Confianza ALTA (texto explícito, fuente 6). Es evidencia **contraria** a tratar los cuidados de género como si fueran de la especie, y por eso cada dato lo declara.
- **H4 — Hay géneros populares sin fuente de cuidados utilizable en esta investigación**, y quedaron fuera: *Cyrtopodium* (69 observaciones), *Malaxis*, *Stelis*, *Specklinia*, *Elleanthus*, *Chysis*, *Dinema*, *Polystachya*, *Acianthera*; *Cypripedium irapeanum* (17) se excluyó porque su tarjeta trata de especies templadas y la AOS remite a literatura especializada, y *Calanthe calanthoides* (25) porque su tarjeta distingue dos formas de crecimiento y no se puede saber cuál corresponde. Confianza ALTA en que faltan; no se afirma que no exista literatura en otros lugares.

## Límites y riesgos

- La lista refleja lo que la gente **observa**, no lo que se **compra o cultiva**. Especies muy populares en cultivo pero poco observadas pueden faltar (no se validó ninguna lista comercial).
- Nombres comunes tomados de iNaturalist (contribuidos por usuarios; solo 40 de 100 tienen uno).
- Nombres científicos como los da iNaturalist; pueden diferir de los aceptados por Kew o de las sinonimias de la AOS (Guarianthe se cita con la hoja de Cattleya; Trichocentrum, con la de Oncidium).
- Evidencia global: **Media/Baja**, sin revisión de un experto botánico.

## Conjunto seleccionado (100)

Géneros: Epidendrum (12), Prosthechea (9), Govenia (5), Trichocentrum (5), Maxillaria (5), Oncidium (4), Sobralia (4), Rhynchostele (3), Bletia (3), Encyclia (3), Stanhopea (3), Lycaste (3), Guarianthe (2), Aulosepalum (2), Pleurothallis (2), Isochilus (2), Laelia (2), Sarcoglottis (2), Dichaea (2), Barkeria (2), Gongora (2), Coelia (2), Scaphyglottis (2), Nidema (1), Catasetum (1), Dichromanthus (1), Domingoa (1), Brassia (1), Cuitlauzina (1), Notylia (1), Lockhartia (1), Sacoila (1), Platystele (1), Clowesia (1), Vanilla (1), Meiracyllium (1), Cycnoches (1), Brassavola (1), Arpophyllum (1), Ionopsis (1), Trichopilia (1), Caularthron (1).

| # | Especie | Observaciones en Chiapas | Nombre común (iNaturalist) |
|--:|---------|-------------------------:|----------------------------|
| 1 | Prosthechea cochleata | 237 | Orquídea Pulpito |
| 2 | Rhynchostele bictoniensis | 184 | — |
| 3 | Epidendrum radicans | 153 | Estrella de fuego |
| 4 | Oncidium sphacelatum | 132 | Orquídea dama amarilla |
| 5 | Bletia purpurea | 123 | Orquídea púrpura |
| 6 | Prosthechea radiata | 116 | Canelita |
| 7 | Prosthechea ochracea | 112 | — |
| 8 | Nidema boothii | 105 | Orquídea enana blanca |
| 9 | Catasetum integerrimum | 104 | Orquídea cola de pato |
| 10 | Govenia liliacea | 104 | Orquídea blanca |
| 11 | Encyclia cordigera | 86 | Flor de Encarnacion |
| 12 | Guarianthe aurantiaca | 79 | Orquídea naranja |
| 13 | Sobralia macrantha | 74 | Flor de un día |
| 14 | Dichromanthus cinnabarinus | 67 | cutzis |
| 15 | Guarianthe skinneri | 61 | Flor de Candelaria |
| 16 | Epidendrum radioferens | 53 | — |
| 17 | Domingoa purpurea | 53 | — |
| 18 | Oncidium leucochilum | 49 | Oncidium de labio blanco |
| 19 | Epidendrum stamfordianum | 49 | Orquídea tropical |
| 20 | Aulosepalum hemichrea | 48 | — |
| 21 | Brassia verrucosa | 46 | Orquídea de verrugas verdes |
| 22 | Trichocentrum ascendens | 46 | — |
| 23 | Maxillaria variabilis | 46 | azucena de monte |
| 24 | Pleurothallis quadrifida | 45 | — |
| 25 | Cuitlauzina pulchella | 45 | — |
| 26 | Prosthechea chacaoensis | 44 | — |
| 27 | Notylia barkeri | 42 | — |
| 28 | Epidendrum ciliare | 39 | orquídea pestañas de dama |
| 29 | Isochilus aurantiacus | 39 | — |
| 30 | Lockhartia oerstedii | 39 | — |
| 31 | Stanhopea graveolens | 39 | — |
| 32 | Rhynchostele stellata | 38 | — |
| 33 | Trichocentrum luridum | 38 | Orquídea enana oreja de mula |
| 34 | Maxillaria egertoniana | 38 | — |
| 35 | Epidendrum cardiophorum | 36 | — |
| 36 | Sacoila lanceolata | 35 | orquidea terciopelo morado |
| 37 | Sobralia decora | 35 | — |
| 38 | Stanhopea oculata | 34 | Tecuanxochitl |
| 39 | Platystele stenostachya | 34 | — |
| 40 | Laelia superbiens | 33 | Palo de águila |
| 41 | Bletia campanulata | 31 | Flor de muertos |
| 42 | Prosthechea varicosa | 30 | — |
| 43 | Govenia superba | 30 | Azucena amarilla |
| 44 | Prosthechea livida | 28 | — |
| 45 | Sarcoglottis sceptrodes | 28 | — |
| 46 | Trichocentrum andreanum | 28 | — |
| 47 | Oncidium sotoanum | 27 | — |
| 48 | Maxillaria elatior | 27 | — |
| 49 | Dichaea muricatoides | 26 | — |
| 50 | Stanhopea saccata | 26 | — |
| 51 | Clowesia russelliana | 25 | — |
| 52 | Epidendrum flexuosum | 25 | — |
| 53 | Maxillaria densa | 25 | Orquídea de mandíbulas |
| 54 | Vanilla planifolia | 24 | Vainilla |
| 55 | Sobralia xantholeuca | 24 | — |
| 56 | Aulosepalum pyramidale | 24 | orquídea blanca piramidal |
| 57 | Encyclia bractescens | 24 | — |
| 58 | Prosthechea panthera | 23 | — |
| 59 | Meiracyllium trinasutum | 22 | — |
| 60 | Sobralia macdougallii | 22 | — |
| 61 | Epidendrum parkinsonianum | 21 | — |
| 62 | Lycaste aromatica | 21 | Canela |
| 63 | Laelia rubescens | 21 | Flor de la concepción |
| 64 | Epidendrum caligarium | 21 | — |
| 65 | Cycnoches ventricosum | 20 | — |
| 66 | Prosthechea rhynchophora | 20 | — |
| 67 | Barkeria spectabilis | 20 | — |
| 68 | Brassavola nodosa | 20 | Dama de noche |
| 69 | Dichaea glauca | 20 | Orquídea terrestre |
| 70 | Govenia alba | 20 | — |
| 71 | Arpophyllum giganteum | 19 | Tzauhxilotl |
| 72 | Gongora unicolor | 19 | — |
| 73 | Ionopsis utricularioides | 18 | Angelitos |
| 74 | Bletia parkinsonii | 18 | — |
| 75 | Coelia macrostachya | 18 | — |
| 76 | Epidendrum nocturnum | 17 | Flor de San Pedro |
| 77 | Rhynchostele cordata | 17 | — |
| 78 | Scaphyglottis crurigera | 17 | — |
| 79 | Pleurothallis matudana | 17 | — |
| 80 | Trichocentrum brachyphyllum | 17 | Chorizo con huevo |
| 81 | Lycaste virginalis | 16 | Monja blanca |
| 82 | Barkeria skinneri | 16 | — |
| 83 | Epidendrum polyanthum | 16 | — |
| 84 | Coelia guatemalensis | 16 | — |
| 85 | Govenia dressleriana | 16 | — |
| 86 | Sarcoglottis schaffneri | 16 | Orquídea Mexicana Terrestre de Lengua Carnosa |
| 87 | Encyclia rodolfoi | 16 | — |
| 88 | Oncidium hintonii | 15 | Orquidia dama danzante |
| 89 | Scaphyglottis fasciculata | 15 | — |
| 90 | Isochilus latibracteatus | 14 | — |
| 91 | Maxillaria meleagris | 14 | — |
| 92 | Epidendrum veroscriptum | 13 | — |
| 93 | Trichocentrum oerstedii | 13 | Oreja de burro |
| 94 | Gongora galeata | 12 | vaquita |
| 95 | Lycaste cruenta | 12 | — |
| 96 | Prosthechea baculus | 12 | — |
| 97 | Trichopilia tortilis | 12 | — |
| 98 | Govenia matudae | 12 | — |
| 99 | Epidendrum cristatum | 12 | — |
| 100 | Caularthron bilamellatum | 11 | — |

## Fuentes

| # | Fuente | Tipo | Nivel |
|--:|--------|------|-------|
| 1 | iNaturalist API, `observations/species_counts`, lugar 97003 (Chiapas), Orchidaceae, grado de investigación, `native=true`, `captive=false`, consultada 2026-09-19 | Base comunitaria con verificación por pares | Medio |
| 2 | American Orchid Society, páginas de género `https://www.aos.org/explore/{género}` (Care and Culture Card) | Organización de referencia | Alto |
| 3 | Solano-Gómez, R. et al. 2016. Diversity and distribution of the orchids of the Tacaná-Boquerón region, Chiapas, Mexico. Botanical Sciences 94(3): 625-664 (325 especies en la región) | Revisada por pares | Muy alto |
| 4 | Catálogo de Orquídeas de Chiapas (referido en una búsqueda; 717 especies): no se pudo leer su texto | Secundaria | Bajo |
| 5 | AOS, hojas de cultivo Oncidium, Cattleya, Gongora, Catasetum y Reedstem Epidendrum Culture, `https://www.aos.org/orchid-care/` | Organización de referencia | Alto |
| 6 | AOS, alianza Cattleya, `https://www.aos.org/explore/alliance/cattleya-alliance` (advertencia sobre su hoja) | Organización de referencia | Alto |

## Dónde aterrizó

- **Work item:** s1.6 (conjunto semilla) de la épica e1: las 100 fichas JSON.
- **Pendiente para el humano:** revisar la regla de popularidad (observaciones en iNaturalist) y aceptar que los cuidados son de género; ambos están dichos en cada ficha y en la retrospectiva de s1.6.
