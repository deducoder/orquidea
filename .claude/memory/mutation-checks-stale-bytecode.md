---
name: mutation-checks-stale-bytecode
description: Al mutar código para verificar pruebas, desactivar bytecode; y ruff formatea los bloques de código de los .md
metadata:
  type: feedback
---

Al hacer mutaciones de verificación (sed sobre el código y pytest), un mutante "sobrevivió" puede ser falso por bytecode obsoleto (mismo tamaño y mismo segundo de mtime): correr con `PYTHONDONTWRITEBYTECODE=1 uv run pytest -p no:cacheprovider` y borrando `__pycache__`.

**Why:** en s1.2 dos mutaciones parecieron sobrevivir y no era cierto; en s3.6 pasó al revés: tras restaurar el archivo, el bytecode del mutante siguió cargándose y el gate falló con una constante ya restaurada.
**How to apply:** toda mutación se verifica sin caché, y tras restaurar se borra `__pycache__` (`find src tests -name __pycache__ -prune -exec rm -rf {} +`) antes de correr el gate. Además `ruff format --check` del gate también revisa los bloques de código de los `.md` (p. ej. `design.md`): escribirlos ya formateados.
