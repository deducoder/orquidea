# Security — Instance binding

> Lo que este proyecto responde a `security-review`: qué escáner corre y cómo
> recibe el alcance del work item. Son hechos de esta instancia, no una regla
> genérica: por eso este archivo vive en el proyecto y no en el plugin.

- **Scanner:** Bandit (análisis estático de seguridad para Python), dependencia
  de desarrollo en `pyproject.toml`; se ejecuta con `uv run bandit`.
- **Scope:** la lista de archivos `.py` que el work item cambió respecto de su
  base, pasada como argumentos posicionales:
  `uv run bandit -q $(git diff --name-only --diff-filter=d {base}...HEAD -- '*.py')`.
  Si la lista sale vacía no hay nada que escanear y **no se invoca**: Bandit sin
  argumentos sale con código 2 (error de uso), no con un resultado limpio.
  Bandit lee los archivos del disco, así que el work item debe estar
  comprometido y sin cambios pendientes al escanear.

## Last verified

2026-09-19: Bandit 1.9.4 corrido sobre un archivo con `subprocess.call(cmd,
shell=True)` plantado reportó B602 (severidad alta, CWE-78) y B404, con código
de salida 1; sobre `src/orquidea/__init__.py` salió limpio con código 0; con una
lista de archivos vacía salió con código 2.
