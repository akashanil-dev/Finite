FROM python:3.13-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.13-slim
RUN groupadd --gid 10001 finite && useradd --uid 10001 --gid finite --create-home finite
WORKDIR /app
COPY --from=build /app/.venv /app/.venv
COPY --chown=finite:finite app ./app
RUN mkdir /data && chown finite:finite /data
ENV PATH="/app/.venv/bin:$PATH" FINITE_DATA_DIR=/data PYTHONUNBUFFERED=1
USER finite
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=4)"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--no-proxy-headers"]
