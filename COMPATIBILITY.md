# Multi-Architecture Compatibility Verification

This project is designed to run on multiple hardware architectures, primarily:
-   **x86_64 (AMD64)**: Standard Linux servers, Intel/AMD desktops.
-   **ARM64 (AArch64)**: Apple Silicon Macs (M1/M2/M3), Raspberry Pi 4/5, AWS Graviton.

## 1. Automated Verification (CI)

We use **GitHub Actions** to automatically verify compatibility on every push.
The workflow file is located at: `.github/workflows/verify-compat.yml`.

-   **x86_64**: Runs natively on `ubuntu-latest` runners.
-   **ARM64**: Can be emulated using QEMU (slow) or run on native ARM runners (if available).

## 2. Manual Verification

If you want to verify compatibility locally (e.g., you are on a Mac M1 but want to test x86 compatibility), you can use Docker's multi-platform capabilities.

### Prerequisites
-   Docker Desktop (Mac/Windows) or Docker Engine with `binfmt-support` (Linux).
-   Enable "Use Rosetta for x86/amd64 emulation on Apple Silicon" in Docker Desktop settings for better performance.

### How to Run Cross-Platform Tests

**1. Test Native Architecture (Default)**
Just run the script normally. It uses your host's architecture.
```bash
python3 run_tests.py
```

**2. Test Emulated Architecture**
To simulate running on a different CPU (e.g., testing x86 behavior on an M1 Mac), set the `DOCKER_DEFAULT_PLATFORM` environment variable.

*Test x86_64 on ARM64 (M1/M2):*
```bash
export DOCKER_DEFAULT_PLATFORM=linux/amd64
python3 run_tests.py --reset
```

*Test ARM64 on x86_64 (Intel):*
```bash
export DOCKER_DEFAULT_PLATFORM=linux/arm64
python3 run_tests.py --reset
```

> **Note**: Emulation is significantly slower. You may need to increase timeouts in `run_tests.py` if services fail to start in time.

## 3. Image Selection Guidelines

To ensure multi-arch compatibility, always choose Docker images that support both `amd64` and `arm64`.

**Safe Bets (Official Images):**
-   `postgres:alpine`
-   `redis:alpine`
-   `nginx:alpine`
-   `busybox`

**Check Image Support:**
You can inspect an image's manifest to see supported architectures:

```bash
docker manifest inspect postgres:16-alpine
```

**Output Example:**
```json
   {
      "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
      "platform": {
         "architecture": "amd64",
         "os": "linux"
      }
   },
   {
      "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
      "platform": {
         "architecture": "arm64",
         "os": "linux"
      }
   }
```
If you see both `amd64` and `arm64`, the image is safe to use.
