# syntax=docker/dockerfile:1
FROM python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN --mount=type=secret,id=proxy_ca \
    if [ -f /run/secrets/proxy_ca ]; then export SSL_CERT_FILE=/run/secrets/proxy_ca; fi; \
    apt-get update && apt-get install -y --no-install-recommends g++ && \
    rm -rf /var/lib/apt/lists/*
RUN groupadd --gid 10001 runner && useradd --uid 10001 --gid runner --no-create-home runner && \
    mkdir /work && chown runner:runner /work
COPY --chmod=0444 solver_judge/sandbox/harness.py solver_judge/bounded.py /opt/solver_judge/
RUN chmod 0555 /opt/solver_judge
USER 10001:10001
WORKDIR /work
ENTRYPOINT ["python", "-B", "/opt/solver_judge/harness.py"]
