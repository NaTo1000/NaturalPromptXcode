# Containers & Kubernetes

NaturalPromptXcode ships with a multi-stage, multi-architecture container
image plus Docker Compose and Kubernetes manifests to run the code-generation
CLI in any container environment.

> **Note** — The container runs the **prompt → Swift / Xcode project
> generation** pipeline. Actually compiling an iOS app with `xcodebuild` still
> requires macOS and is **not** performed inside this Linux container.

## Files

| Path                       | Purpose                                          |
|----------------------------|--------------------------------------------------|
| `Dockerfile`               | Multi-stage, buildx-ready image definition       |
| `.dockerignore`            | Keeps the image lean and free of local secrets   |
| `docker-compose.yml`       | Local orchestration / dev workflow               |
| `scripts/docker-buildx.sh` | Helper that drives `docker buildx` for multi-arch builds |
| `k8s/`                     | Namespace, ConfigMap, Secret, PVC, Deployment, Service, Job, Kustomization |

## 1. Build with Docker Buildx

```bash
# One-time: ensure buildx is available
docker buildx version

# Local build (current arch, loaded into the daemon)
./scripts/docker-buildx.sh

# Multi-arch build pushed to a registry
IMAGE=ghcr.io/nato1000/naturalpromptxcode \
TAG=0.1.0 \
PLATFORMS=linux/amd64,linux/arm64 \
PUSH=1 \
    ./scripts/docker-buildx.sh
```

Equivalent raw command:

```bash
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t ghcr.io/nato1000/naturalpromptxcode:0.1.0 \
    --push .
```

## 2. Run with Docker

```bash
docker run --rm -it \
    -e OPENAI_API_KEY="$OPENAI_API_KEY" \
    -v "$PWD/output:/data/output" \
    naturalpromptxcode:latest \
    generate "A simple todo list app" --output /data/output
```

## 3. Run with Docker Compose

```bash
# Build
docker compose build

# One-shot generation
OPENAI_API_KEY=sk-... docker compose run --rm npx \
    generate "A weather app with SwiftUI" --output /data/output
```

Generated projects appear under `./output/` on the host.

## 4. Deploy to Kubernetes

```bash
# 1. Create the namespace + workload
kubectl apply -k k8s/

# 2. Create your real API-key secret (do NOT use the example file as-is)
kubectl -n naturalpromptxcode create secret generic npx-secrets \
    --from-literal=OPENAI_API_KEY="sk-..." \
    --from-literal=ANTHROPIC_API_KEY=""

# 3. Use the long-running pod interactively
kubectl -n naturalpromptxcode exec -it deploy/naturalpromptxcode -- \
    naturalpromptxcode generate "A todo list app" --output /data/output

# 4. Or submit a one-shot Job
kubectl -n naturalpromptxcode create -f k8s/job.example.yaml
kubectl -n naturalpromptxcode logs -f -l app.kubernetes.io/component=job
```

### Customising the image

The Kustomization references the `naturalpromptxcode:latest` image. Point it
at your registry without editing manifests:

```bash
cd k8s
kustomize edit set image naturalpromptxcode=ghcr.io/nato1000/naturalpromptxcode:0.1.0
kubectl apply -k .
```

### Security defaults

The Deployment and Job templates run as a non-root user (UID 1000), drop all
Linux capabilities, disallow privilege escalation, and mount the root
filesystem read-only with writable `emptyDir` volumes for `/tmp` and the
output PVC. Adjust these to fit your cluster's PodSecurity / OPA policies.
