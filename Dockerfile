# syntax=docker/dockerfile:1

# The official Python image is multi-architecture, so Docker can select the
# correct image for AMD64 or ARM64 hosts automatically.
ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    HOME=/app \
    XDG_CACHE_HOME=/app/.cache \
    PORT=5050

WORKDIR /app

# libgomp1 is required by FAISS at runtime. Build tools provide a fallback for
# Python packages that do not publish a wheel for the current architecture.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies before copying the application to improve build caching.
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install --prefer-binary -r requirements.txt

# Copy only the files needed at runtime. Secrets must be supplied with
# --env-file or -e when the container is started.
COPY app/ ./app/
COPY data/ ./data/
COPY vectorstore/ ./vectorstore/

# Run as an unprivileged user while keeping the log directory writable.
RUN addgroup --system appuser \
    && adduser --system --ingroup appuser appuser \
    && mkdir -p /app/logs /app/.cache \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 5050

# Flask's CLI lets deployments override PORT without changing application code.
CMD ["sh", "-c", "exec python -m flask --app app.application run --host=0.0.0.0 --port=${PORT:-5050}"]
