# CVLN Academy — NVIDIA Accelerated Runtime Architecture

**Status:** IMPLEMENTED / GPU ACTIVATION REQUIRES TARGET-HOST PROOF  
**Owner:** CVLN Academy Platform Engineering  
**Last reviewed:** 2026-09-12  
**Architecture version:** 1.0  
**Scope:** CUDA, RAPIDS cuDF, NVIDIA Dynamo, Jetson edge profile

---

## 1. Executive decision

CVLN Academy uses NVIDIA acceleration as a **separate, observable execution plane**, not as a mandatory dependency of the public web application.

The architecture optimizes for two outcomes at the same time:

1. **maximum throughput where GPU acceleration is economically and technically justified**;
2. **no regression of the CPU web runtime, CI, or business-critical Academy paths when a GPU is absent**.

The platform therefore distinguishes five states that must never be collapsed into one label:

| State | Meaning |
|---|---|
| `configured` | An operator supplied configuration. |
| `installed` | A software package is present. |
| `detected` | Runtime evidence proves the hardware/software is usable enough to be discovered. |
| `selected` | Academy is configured to route a workload to the component. |
| `active` / `verified` | A real request executed through that component and passed a result check. |

A component is **not production-verified** merely because its dependency exists in a file or its environment variable is set.

---

## 2. Why this architecture

### 2.1 GPU everywhere would be slower and less reliable

Many Academy operations are small CRUD, authorization, billing, legal acceptance, progression, routing, or MongoDB operations. Moving these to GPU adds serialization, transfer, initialization, and scheduling overhead without useful parallelism.

For tabular workloads, CVLN Academy therefore uses an adaptive threshold:

```text
small workload
    -> Python / CPU
large workload
    -> detect NVIDIA GPU
    -> detect importable cuDF
    -> execute cuDF
    -> on optional-mode failure: CPU fallback + reason
    -> on required-mode failure: fail closed
```

The default threshold is `50,000` rows and is operator-configurable through `NVIDIA_CUDF_MIN_ROWS`. It is a starting policy, not a universal performance truth. Production benchmarks must tune it per GPU, dataset width, transformation mix, and transfer cost.

### 2.2 The web service and inference service have different scaling characteristics

FastAPI/MongoDB Academy traffic and LLM inference do not scale the same way. NVIDIA Dynamo is therefore treated as a **separate inference plane** accessed through an OpenAI-compatible HTTP boundary.

This permits:

- independent GPU autoscaling;
- independent inference engine selection;
- independent model lifecycle;
- explicit latency and availability SLOs;
- web deployments without CUDA libraries;
- replacement or upgrade of the inference fleet without changing Academy persona/business logic.

### 2.3 Jetson is an edge target, not a cloud acceleration flag

`JETSON_EDGE_MODE=true` does not make a host a Jetson. Academy reports Jetson `active=true` only when edge mode was requested **and** runtime host evidence identifies a Jetson platform.

That prevents a deployment variable from becoming fake hardware evidence.

---

## 3. Current implementation

### 3.1 Code paths

| Capability | Implementation | Runtime entry point |
|---|---|---|
| NVIDIA/CUDA detection | `backend/services/nvidia_runtime.py` | `nvidia-smi` evidence |
| cuDF detection | `backend/services/nvidia_runtime.py` | import + CUDA evidence |
| Adaptive tabular acceleration | `accelerated_group_count()` | Python or cuDF |
| Dynamo inference client | `DynamoClient` | OpenAI-compatible `/v1/chat/completions` |
| Academy AI transport selection | `backend/services/agent_factory.py` | `ACADEMY_AI_TRANSPORT` |
| Public accelerator status | `backend/api/accelerators.py` | `GET /api/accelerators/status` |
| Operator diagnostics | same | `GET /api/accelerators/diagnostics` |
| Executable accelerator proof | same | `POST /api/accelerators/self-test` |
| CUDA 13 dependency profile | `backend/requirements-gpu-cu13.txt` | GPU worker build |
| CUDA 12 compatibility profile | `backend/requirements-gpu-cu12.txt` | qualified legacy GPU worker |
| Contract CI | `.github/workflows/nvidia-accelerated-runtime-ci.yml` | pull request / main |

The `accelerators` router is included by `backend/api/__init__.py`; it is therefore part of the aggregate `/api` surface rather than a detached source file.

---

## 4. CUDA baseline

### 4.1 Preferred new-fleet baseline

For new GPU workers, Academy targets **CUDA 13**. The repository keeps CUDA 12 as a compatibility profile for an already-qualified fleet.

NVIDIA documents that CUDA 13.x requires an NVIDIA driver in the R580 family or newer for minor-version compatibility; later CUDA 13 releases can require newer branches for newly introduced capabilities. The exact driver/toolkit pair must be qualified on the target fleet rather than inferred from package metadata.

Official references:

- NVIDIA CUDA Toolkit release notes: <https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/>
- CUDA compatibility guide: <https://docs.nvidia.com/deploy/cuda-compatibility/latest/>
- CUDA Linux installation guide: <https://docs.nvidia.com/cuda/cuda-installation-guide-linux/>

### 4.2 Runtime proof

The Academy detector calls `nvidia-smi` with a bounded timeout and records:

- GPU name;
- driver version;
- total GPU memory;
- GPU count.

Absence or failure of `nvidia-smi` is not treated as a GPU success.

---

## 5. RAPIDS cuDF

### 5.1 Version policy

The accelerated profiles pin the current stable RAPIDS cuDF release verified during this change:

```text
cudf-cu13==26.8.1
cudf-cu12==26.8.1
```

The GPU packages are intentionally absent from `backend/requirements.txt`.

RAPIDS packages contain large native dependencies. Adding them to every Render/CI/web image would increase build time and attack surface and can make a CPU deployment less reliable without accelerating its normal request path.

Official references:

- RAPIDS release schedule: <https://docs.rapids.ai/releases/schedule/>
- cuDF project: <https://docs.rapids.ai/api/cudf/stable/>

### 5.2 Activation policy

A workload reaches cuDF only when all relevant conditions are true:

1. workload is at or above the configured threshold, or an authorized self-test explicitly requires GPU;
2. CUDA-capable NVIDIA hardware is detected;
3. cuDF is installed and importable;
4. the cuDF operation completes successfully.

The API returns the engine that **actually executed** (`python` or `cudf`) plus the fallback reason when applicable.

### 5.3 Required-mode proof

On a real GPU host, an operator can call:

```http
POST /api/accelerators/self-test
Authorization: Bearer <admin|super_admin|founder token>
Content-Type: application/json

{
  "rows": 100000,
  "require_gpu": true
}
```

A valid GPU proof requires all of the following:

```json
{
  "engine": "cudf",
  "fallback_reason": null,
  "checksum": 100000,
  "verified": true
}
```

If CUDA/cuDF is unavailable, `require_gpu=true` fails rather than reporting a CPU result as GPU acceleration.

---

## 6. NVIDIA Dynamo inference plane

### 6.1 Role

Dynamo is used for **high-throughput/low-latency generative AI serving**, not for the FastAPI web runtime itself.

Academy sends assistant traffic through a transport boundary:

```text
assistant persona / mentor
        |
        v
services.ai_assistant
        |
        v
services.agent_factory
        |
        +--> anthropic   (default fallback)
        |
        +--> dynamo      (selected GPU inference plane)
```

NVIDIA Dynamo supports OpenAI-compatible inference frontends and is designed for distributed serving, routing, KV-cache-aware operation, and scalable inference engines.

Official references:

- Dynamo documentation: <https://docs.nvidia.com/dynamo/>
- Dynamo compatibility matrix: <https://docs.nvidia.com/dynamo/latest/reference/compatibility>

### 6.2 Configuration

```env
ACADEMY_AI_TRANSPORT=dynamo
ACADEMY_AI_STRICT=false
NVIDIA_DYNAMO_BASE_URL=http://dynamo-frontend:8000
NVIDIA_DYNAMO_MODEL=<served-model-name>
NVIDIA_DYNAMO_API_KEY=<secret-if-required>
NVIDIA_DYNAMO_CHAT_PATH=/v1/chat/completions
NVIDIA_DYNAMO_TIMEOUT_SECONDS=30
```

Secrets must be stored in the deployment provider's secret/environment system; never commit them.

### 6.3 Fallback and strict modes

**Default (`ACADEMY_AI_STRICT=false`)**

- Dynamo selected;
- request attempts Dynamo;
- if Dynamo is unavailable, Academy logs the failure and uses the configured Anthropic fallback.

**Strict (`ACADEMY_AI_STRICT=true`)**

- Dynamo selected;
- a Dynamo failure does not silently move traffic to another inference provider;
- user receives a controlled temporary-unavailability response.

Strict mode is appropriate where provider/model consistency is more important than availability.

---

## 7. Jetson edge profile

Jetson is reserved for future Academy edge workloads where local compute materially changes the product, for example:

- on-site classroom media analysis;
- low-latency local inference;
- constrained-connectivity deployments;
- local vision/video processing;
- controlled kiosk or studio installations.

It is **not** the primary backend host for billing, identity, entitlements, or canonical MongoDB state.

The current repository implementation provides truthful host detection and an explicit edge-mode contract. It does **not** claim that a Jetson device has been provisioned, flashed, benchmarked, or deployed.

Before production edge activation, the required evidence is:

1. exact Jetson SKU;
2. JetPack/L4T version;
3. CUDA/TensorRT compatibility;
4. power mode and thermal policy;
5. storage endurance/capacity;
6. secure boot and update strategy where applicable;
7. measured model latency/throughput/memory;
8. offline/online reconciliation behavior;
9. remote observability and rollback.

---

## 8. Runtime truth and previous defect

### 8.1 Defect found

Before this work, `CVLN_AGENT_FACTORY_URL` caused `agent_factory.is_remote_enabled()` to return true, but `chat_reply()` did not execute any HTTP request to Agent Factory. The boolean represented **configuration**, not an active remote code path.

### 8.2 Why this defect happens

This defect class appears when a system collapses multiple lifecycle states:

```text
variable exists
    -> assumed configured
    -> assumed wired
    -> assumed active
    -> assumed production-proven
```

Those implications are invalid.

### 8.3 Prevention rule

Every external integration must expose, when meaningful:

```text
configured != reachable != selected != active != verified
```

The health surface now keeps the legacy field for compatibility but adds explicit `agent_factory_remote_configured` and `agent_factory_remote_active` states. Until the Agent Factory API contract is implemented, `active` remains false.

No remote Agent Factory endpoint was invented during this change.

---

## 9. Security controls

### 9.1 Diagnostics

- coarse accelerator status is public;
- full hardware/software diagnostics require `admin`, `super_admin`, or `founder`;
- executable self-test requires the same roles;
- self-test input is bounded to a maximum of one million synthetic rows;
- diagnostics never return API keys;
- Dynamo URL diagnostics strip user information, password, path, query, and fragment.

### 9.2 External inference

Production deployments should additionally enforce:

- TLS for cross-host Dynamo communication;
- network allowlisting/private networking where available;
- secret rotation;
- request/response logging policy that does not leak learner data;
- model-level authorization if several models share the inference plane;
- rate limiting and concurrency controls;
- timeout, retry, circuit-breaker and overload policy at the platform edge.

### 9.3 GPU host isolation

Do not treat a GPU node as a generic public web node. Prefer a dedicated worker/inference network boundary with the minimum required inbound surface.

---

## 10. Performance engineering policy

"GPU enabled" is not a performance result.

For every accelerated workload, compare:

- p50/p95/p99 latency;
- throughput;
- queue time;
- GPU utilization;
- GPU memory utilization;
- CPU utilization;
- host memory;
- data-transfer time;
- initialization/warmup time;
- cost per completed unit of work;
- error/fallback rate.

The cuDF threshold must be changed only from benchmark evidence.

For Dynamo, track at minimum:

- time to first token;
- inter-token latency;
- request throughput;
- tokens/second;
- queue delay;
- cache reuse where available;
- model worker saturation;
- fallback rate;
- timeout/error rate.

---

## 11. CI and verification ladder

Academy uses a proof ladder instead of one ambiguous green check:

```text
source exists
  -> import succeeds
  -> router includes endpoint
  -> unit contract passes
  -> CPU fallback truth passes
  -> base platform CI passes
  -> GPU image builds
  -> CUDA detected on target host
  -> cuDF required self-test executes with engine=cudf
  -> workload benchmark beats CPU baseline
  -> production canary passes
```

The GitHub-hosted CI is not a GPU proof because the normal Ubuntu runners are CPU hosts. It verifies CPU portability, route reachability, security/redaction, fail-closed behavior, and dependency-profile isolation.

---

## 12. Deployment profiles

### A. Current web/API profile

```text
FastAPI + MongoDB
CPU runtime
no cuDF dependency
Anthropic transport unless changed
```

### B. GPU analytics worker

```text
Python 3.12
CUDA 13 qualified driver/runtime
requirements-gpu-cu13.txt
NVIDIA_CUDF_MIN_ROWS tuned from benchmark
NVIDIA_ACCELERATION_REQUIRED according to workload criticality
```

### C. Dynamo inference cluster

```text
NVIDIA GPU nodes
Dynamo frontend + selected inference engine
private/controlled network endpoint
Academy ACADEMY_AI_TRANSPORT=dynamo
```

### D. Jetson edge node

```text
qualified Jetson + JetPack/L4T
JETSON_EDGE_MODE=true
edge-only workload
canonical state remains server-side unless an explicit offline-reconciliation design is approved
```

---

## 13. Rollout plan

1. Merge only after CPU contract CI and full platform CI are green.
2. Keep `ACADEMY_AI_TRANSPORT=anthropic` in existing production until Dynamo exists.
3. Provision a qualified CUDA 13 GPU worker.
4. Install `requirements-gpu-cu13.txt`.
5. Call diagnostics and required self-test.
6. Benchmark representative Academy tabular workloads against CPU.
7. Tune `NVIDIA_CUDF_MIN_ROWS` from evidence.
8. Deploy Dynamo separately and verify its health/model endpoint.
9. Canary a limited portion of assistant traffic.
10. Compare latency, quality, errors, cost, and fallback rate.
11. Increase traffic only if SLOs improve.
12. Treat Jetson as a separate edge program with device-specific qualification.

---

## 14. Rollback

The architecture is deliberately reversible:

- set `ACADEMY_AI_TRANSPORT=anthropic` to remove Dynamo from the assistant request path;
- do not install the GPU requirements profile on CPU nodes;
- lower operational risk by leaving `NVIDIA_ACCELERATION_REQUIRED=false` for optional workloads;
- remove a GPU worker from the queue without changing the public API;
- set `JETSON_EDGE_MODE=false` to disable the requested edge profile.

No canonical Academy learner, billing, legal, or identity data is moved into NVIDIA-specific storage by this implementation.

---

## 15. Acceptance criteria for “NVIDIA production verified”

Do **not** mark the NVIDIA runtime VERIFIED until target-host evidence proves:

- [ ] NVIDIA GPU detected with expected model and driver;
- [ ] qualified CUDA version;
- [ ] cuDF imports successfully;
- [ ] `POST /api/accelerators/self-test` with `require_gpu=true` returns `engine=cudf` and `verified=true`;
- [ ] benchmark demonstrates benefit on a representative Academy workload;
- [ ] Dynamo endpoint is reachable if Dynamo is selected;
- [ ] a real assistant request returns through Dynamo with expected model;
- [ ] failure/fallback behavior is tested;
- [ ] observability is receiving latency/error/fallback metrics;
- [ ] secrets and network boundaries have been reviewed;
- [ ] rollback has been executed at least once in staging;
- [ ] production canary is green.

Until those checks exist, the correct state is **IMPLEMENTED**, not VERIFIED.
