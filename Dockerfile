FROM python:3.13-slim

ENV UV_PYTHON_DOWNLOADS=never \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN pip install --no-cache-dir uv==0.12.7

COPY pyproject.toml uv.lock ./
COPY src ./src

RUN uv sync --frozen --no-dev \
    && useradd --system --uid 10001 app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD python -c "import urllib.request as u; u.urlopen('http://127.0.0.1:8000/salud')"

CMD ["uvicorn", "orquidea.web.app:app", "--host", "0.0.0.0", "--port", "8000"]
