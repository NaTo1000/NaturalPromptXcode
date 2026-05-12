# syntax=docker/dockerfile:1.7
#
# NaturalPromptXcode container image.
#
# Multi-stage, multi-arch image designed to be built with Docker Buildx:
#
#   docker buildx build \
#       --platform linux/amd64,linux/arm64 \
#       -t naturalpromptxcode:latest \
#       --load .
#
# The image bundles the Python CLI and exposes it as the default entrypoint.
# Note: actual `xcodebuild` execution requires macOS and cannot run inside
# this Linux container. The container is intended for the code-generation
# pipeline (prompt -> Swift sources / Xcode project files).

ARG PYTHON_VERSION=3.11

# ---------------------------------------------------------------------------
# Stage 1: builder - install Python dependencies into a virtualenv
# ---------------------------------------------------------------------------
FROM --platform=$BUILDPLATFORM python:${PYTHON_VERSION}-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install build tools required for any packages that need compilation.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
 && rm -rf /var/lib/apt/lists/*

# Create an isolated virtualenv so we can copy it cleanly into the final stage.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies first to maximise Docker layer caching.
COPY requirements.txt ./
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy the project sources and install the package itself.
COPY setup.py README.md config.yaml.example ./
COPY src ./src
COPY naturalpromptxcode.py ./
RUN pip install .

# ---------------------------------------------------------------------------
# Stage 2: runtime - minimal image with just the venv and the app
# ---------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS runtime

ARG APP_USER=npx
ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    NPX_OUTPUT_DIR=/data/output \
    NPX_CONFIG=/etc/naturalpromptxcode/config.yaml

# Create an unprivileged user to run the application.
RUN groupadd --system --gid "${APP_GID}" "${APP_USER}" \
 && useradd  --system --uid "${APP_UID}" --gid "${APP_GID}" \
        --home-dir /home/${APP_USER} --create-home --shell /usr/sbin/nologin \
        "${APP_USER}"

# Copy the prepared virtualenv and the application from the builder.
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /build /opt/naturalpromptxcode

# Provide a default config and a writable output directory.
RUN mkdir -p /etc/naturalpromptxcode /data/output \
 && cp /opt/naturalpromptxcode/config.yaml.example /etc/naturalpromptxcode/config.yaml \
 && chown -R "${APP_USER}:${APP_GID}" /data /etc/naturalpromptxcode

WORKDIR /opt/naturalpromptxcode
USER ${APP_USER}

VOLUME ["/data/output", "/etc/naturalpromptxcode"]

# Basic healthcheck: the CLI should be importable and respond to --help.
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import src.main" || exit 1

ENTRYPOINT ["naturalpromptxcode"]
CMD ["--help"]
