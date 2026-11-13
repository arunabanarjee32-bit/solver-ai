# syntax=docker/dockerfile:1
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
RUN --mount=type=secret,id=proxy_ca \
    if [ -f /run/secrets/proxy_ca ]; then \
      export PIP_CERT=/run/secrets/proxy_ca SSL_CERT_FILE=/run/secrets/proxy_ca; \
    fi; \
    pip install --no-cache-dir uv==0.13.6
COPY pyproject.toml uv.lock ./
RUN --mount=type=secret,id=proxy_ca \
    if [ -f /run/secrets/proxy_ca ]; then export SSL_CERT_FILE=/run/secrets/proxy_ca; fi; \
    uv sync --frozen --no-dev --no-install-project
COPY --chown=10001:10001 solver_api ./solver_api
RUN groupadd --gid 10001 solver && useradd --uid 10001 --gid solver --no-create-home solver \
    && mkdir -p /app/.local && chown 10001:10001 /app/.local
USER solver
EXPOSE 8000
CMD ["/app/.venv/bin/uvicorn", "solver_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
