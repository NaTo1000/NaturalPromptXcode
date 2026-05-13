#!/usr/bin/env bash
#
# Build a multi-architecture image for NaturalPromptXcode using Docker Buildx.
#
# Examples:
#   # Build locally for the current platform and load into the local daemon.
#   ./scripts/docker-buildx.sh
#
#   # Build and push a multi-arch image to a registry.
#   IMAGE=ghcr.io/nato1000/naturalpromptxcode TAG=0.1.0 PUSH=1 \
#       ./scripts/docker-buildx.sh
#
# Environment variables:
#   IMAGE      Image name (default: naturalpromptxcode)
#   TAG        Image tag (default: latest)
#   PLATFORMS  Comma-separated buildx platforms (default: linux/amd64,linux/arm64)
#   PUSH       If "1", push the manifest to the registry; otherwise --load locally.
#   BUILDER    Name of the buildx builder to use/create (default: npx-builder)

set -euo pipefail

IMAGE="${IMAGE:-naturalpromptxcode}"
TAG="${TAG:-latest}"
PLATFORMS="${PLATFORMS:-linux/amd64,linux/arm64}"
PUSH="${PUSH:-0}"
BUILDER="${BUILDER:-npx-builder}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if ! docker buildx version >/dev/null 2>&1; then
    echo "error: docker buildx is not available. Install Docker 20.10+ or the buildx plugin." >&2
    exit 1
fi

# Create (idempotently) and select a dedicated builder instance.
if ! docker buildx inspect "${BUILDER}" >/dev/null 2>&1; then
    echo ">>> Creating buildx builder '${BUILDER}'"
    docker buildx create --name "${BUILDER}" --driver docker-container --use
else
    docker buildx use "${BUILDER}"
fi
docker buildx inspect --bootstrap >/dev/null

OUTPUT_FLAG="--load"
if [[ "${PUSH}" == "1" ]]; then
    OUTPUT_FLAG="--push"
fi

# --load only supports a single platform; fall back to the host platform.
if [[ "${OUTPUT_FLAG}" == "--load" && "${PLATFORMS}" == *","* ]]; then
    HOST_ARCH="$(uname -m)"
    case "${HOST_ARCH}" in
        x86_64)  PLATFORMS="linux/amd64" ;;
        aarch64|arm64) PLATFORMS="linux/arm64" ;;
        *) PLATFORMS="linux/amd64" ;;
    esac
    echo ">>> --load requested: restricting platforms to ${PLATFORMS}"
fi

echo ">>> Building ${IMAGE}:${TAG} for ${PLATFORMS} (${OUTPUT_FLAG})"
docker buildx build \
    --platform "${PLATFORMS}" \
    --tag "${IMAGE}:${TAG}" \
    --file "${REPO_ROOT}/Dockerfile" \
    "${OUTPUT_FLAG}" \
    "${REPO_ROOT}"

echo ">>> Done."
