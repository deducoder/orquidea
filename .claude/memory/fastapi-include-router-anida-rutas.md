---
name: fastapi-include-router-anida-rutas
description: "En FastAPI 0.141 app.routes trae _IncludedRouter, no APIRoute; para enumerar rutas hay que entrar en original_router.routes"
metadata:
  type: project
---

Tras `app.include_router(router)`, `app.routes` contiene objetos `_IncludedRouter` (con `original_router.routes`), no las `APIRoute` del router. Una prueba que filtra `isinstance(ruta, APIRoute)` sobre `app.routes` ve solo las rutas definidas directamente en `app`.

**Why:** descubierto en s3.1 de orquidea al dividir `app.py`: `test_web_proteccion.py` se quedó con 0 rutas protegidas.
**How to apply:** usar `tests/fabricas.py::rutas_registradas(app.routes)`, que entra en los routers incluidos, en toda prueba que enumere rutas. Ver [[starlette-testclient-httpx2]] para las pruebas web.
