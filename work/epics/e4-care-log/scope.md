# Epic e4: Care log — Scope

## Objective

El coleccionista registra los riegos y las floraciones de cada ejemplar y, en su ficha, ve el historial en orden cronológico y la fecha del último riego, en lugar de acordarse.

**Value:** cada planta acumula su propia historia y se sabe cuándo se regó por última vez y cuándo floreció; se cumplen RF-06 y RF-07 y se completa el alcance de la versión 0.2.0.

## Stories

| ID | Story | Size | Description |
|----|-------|:----:|-------------|
| s4.1 | Riegos: dominio y almacenamiento | S | Migración `0004` (`riegos`, con baja en cascada), reglas de la fecha (formato y no futura), y agregar, listar, último y quitar (ADR-008; RF-06). |
| s4.2 | Riegos en la ficha del ejemplar | M | Router `cuidados`; la ficha muestra el historial de riegos y la fecha del último, con formulario para registrar y botón para quitar cada uno (RF-06). |
| s4.3 | Floraciones: dominio y almacenamiento | S | Migración `0005` (`floraciones`, con baja en cascada y `fin >= inicio`), reglas de las fechas, y agregar, terminar, listar y quitar (ADR-008; RF-07). |
| s4.4 | Floraciones en la ficha del ejemplar | M | La ficha muestra el historial de floraciones (en curso o terminadas), con formularios para registrar, fijar el fin y quitar (RF-07). |
| s4.5 | Último riego en "Mi colección" | S | La lista muestra la fecha del último riego de cada ejemplar con una sola consulta (RF-06). |
| s4.6 | Medición del peso y guía | S | Script que mide la ficha con el historial lleno y su tope, presupuesto en el gate, y README con el historial (`must-perf-001`). |

Dependencias: s4.2 de s4.1; s4.3 de s4.1 (numeración de migraciones); s4.4 de s4.2 y s4.3; s4.5 de s4.1; s4.6 de s4.4. Sin ciclos. Van en serie: s4.2 y s4.4 tocan la misma ficha y el mismo router.

## In scope

- **MUST:** registrar y quitar riegos por ejemplar, con fecha de calendario no futura; ver el historial de riegos y la fecha del último en la ficha (RF-06); registrar floraciones con inicio y fin opcional, fijar el fin después y quitarlas; ver su historial (RF-07); ambos historiales en orden cronológico; quitar un ejemplar borra su historial; toda ruta nueva exige sesión y, las que escriben, el token CSRF; un tope de registros por ejemplar y tipo, para acotar la página.
- **SHOULD:** la fecha del último riego en "Mi colección"; mensajes claros en español ante fechas inválidas; medición del peso de la ficha con el historial lleno.

## Out of scope

- Fertilización y notas por fecha — no-go del brief (entrada del parking lot aparcada por el humano al declarar v0.2.0) — **never** en esta versión.
- Recordatorios o avisos de riego — no-go del brief (system-context: sin notificaciones) — **never**.
- Estadísticas o gráficas de cuidados — no-go del brief — **never**.
- Modelo genérico de eventos — rabbit hole del brief y opción (A) descartada en ADR-008 — **not now**.
- Registrar riegos de varios ejemplares a la vez — rabbit hole del brief — **not now**.
- Editar un registro ya guardado — RF-06 y RF-07 piden registrar y ver; un error se corrige quitando el registro y agregándolo de nuevo — **not now**.
- Hora del riego o zona horaria del usuario — el registro es un día de calendario (ADR-008) — **not now**.
- Calendario o vista mezclada de toda la colección — RF-06 y RF-07 hablan de la ficha de un ejemplar — **not now**.

## Done when

- [stated] Registrar un riego en un ejemplar y ver la fecha del último riego en su ficha (métrica líder del brief, RF-06), demostrado por una prueba automatizada de extremo a extremo y por el recorrido manual de `story-implement`.
- [stated] La ficha de un ejemplar con 50 registros entre riegos y floraciones los muestra en orden cronológico y su primera carga transfiere ≤ 200 KB (métrica rezagada del brief, `must-perf-001`). El peso en bytes se mide por script en s4.6; la medición con "Slow 3G" en el navegador solo la puede hacer el humano con la aplicación desplegada: **stop previsible** (P4 en `epic-review`).
- [deduced] Una fecha con formato inválido, inexistente o posterior a hoy se rechaza con un mensaje claro y no cambia la base; en una floración, un fin anterior al inicio también (ADR-008).
- [deduced] Un ejemplar que ya tiene el tope de registros de un tipo rechaza uno más con un mensaje claro; el tope acota el peso de la ficha.
- [deduced] Quitar un ejemplar borra sus riegos y floraciones; quitar un registro no toca los de otros ejemplares ni los de otro tipo (ADR-008).
- [deduced] Sin sesión, ninguna ruta de cuidados responde; todo registro, fin o borrado exige el token CSRF; un id de ejemplar o de registro inexistente da 404 y nunca un registro de otro ejemplar (`should-security-002`).
- [deduced] El texto que llega en un formulario nunca se interpreta: solo se aceptan fechas ISO y se muestran con el escape de la plantilla.
- [deduced] Las migraciones `0004` y `0005` se aplican sobre una base de e3 con datos sin perderlos (ADR-003).
- [stated] All stories complete · docs updated · retrospective done

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|------------|
| La medición de `must-perf-001` con "Slow 3G" depende del humano y de un navegador con herramientas de desarrollo (e1, e2 y e3 la descubrieron tarde) | H | M | Prevista desde aquí como stop P4 en `epic-review`; el peso en bytes se mide por script en s4.6 con el tope de registros |
| El historial crece sin límite y engorda la ficha | M | M | Tope de registros por ejemplar y tipo desde s4.1; s4.6 mide la ficha con el tope lleno, y se dimensiona desde el diseño de s4.1 (memoria del proyecto sobre medir con el tamaño máximo) |
| Una fecha mal validada (futura, imposible, en otra zona) contamina el orden y "el último riego" | M | M | Validación en el dominio con `date.fromisoformat`; ADR-008 fija "hoy" del servidor; pruebas de límites en s4.1 y s4.3 |
| Los routers de la ficha se cruzan: `/coleccion/{id}/riegos` frente a `/coleccion/{id}` y `/coleccion/nuevo` | L | M | Router `cuidados` aparte; prueba explícita del orden y de `rutas_registradas` (no `app.routes`) en s4.2 |
| Un registro de otro ejemplar se quita al pasar su id (IDOR) | M | H | Toda consulta de escritura filtra por `ejemplar_id` y `id`; prueba con dos ejemplares en s4.1 y s4.2, y ASVS L2 recorrido desde el diseño de cada historia |
