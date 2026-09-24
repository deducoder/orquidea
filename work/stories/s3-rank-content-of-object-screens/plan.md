# Story s3: Rank content of object screens — Plan

La historia no escribe código. La verificación es `inventory-sources.py` y el comando de G2, los dos vistos en rojo en ADR-018, más `./scripts/check` antes de cada commit.

| # | Tarea | Verificación | Commit |
|---|-------|--------------|--------|
| T1 | La guía con la opción que elija el dueño, `signed-by` según su respuesta, y las otras dos en *What was tried and rejected* | G1 exit 0 con 4 pantallas guiadas; G2 exit 0 | `docs(identity): rank the object screens` |
| T2 | La rejilla de ADR-018 llena y el registro en `accepted` | ninguna celda `pending` | `docs(s3): accept ADR-018` |
| T3 | `survival-review` sobre la guía, con las firmas del dueño | población contada; `precedence` leído | en `chore(s3): review` |
