# ==============================================================================
# Multi-Stage Dockerfile for DevOps Todo Management REST API
# Stage 1: Build & Dependencies Resolution
# Stage 2: Minimal, Hardened Production Runtime (Enhancement)
# ==============================================================================

# ----------------- Stage 1: Builder Stage -----------------
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specifications
COPY requirements.txt .

# Install dependencies into wheels directory to avoid compiling in runtime
RUN python -m pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt


# ----------------- Stage 2: Production Runtime -----------------
FROM python:3.12-slim AS runtime

LABEL maintainer="Gautam Rajesh (1MS24CI045) <1ms24ci045@msrit.edu>" \
      description="Production container for Todo API Microservice" \
      version="1.0.0"

# Set secure execution environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    APP_ENV=production \
    LOG_LEVEL=INFO

WORKDIR /app

# Create unprivileged system user for container security
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/false appuser

# Copy wheels from builder stage and install
COPY --from=builder /build/wheels /wheels
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels requirements.txt

# Copy application source code
COPY --chown=appuser:appgroup app/ ./app/

# Switch to unprivileged user
USER appuser:appgroup

# Expose microservice listening port
EXPOSE 5000

# Container Healthcheck (matches Kubernetes probe behavior)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health').read()" || exit 1

# Production WSGI server execution
ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "30", "--access-logfile", "-", "app.app:app"]
