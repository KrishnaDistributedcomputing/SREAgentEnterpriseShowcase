FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /workspace

COPY pyproject.toml README.md ./
COPY src ./src
COPY apps ./apps

RUN pip install --no-cache-dir .

RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health/live', timeout=2)"

CMD ["uvicorn", "sre_showcase.app:create_app_from_environment", "--factory", "--host", "0.0.0.0", "--port", "8080"]

