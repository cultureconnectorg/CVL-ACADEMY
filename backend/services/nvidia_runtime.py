"""NVIDIA accelerated-compute boundary for CVLN Academy.

The Academy web runtime must stay portable: CPU-only Render/CI deployments remain
valid, while CUDA/cuDF-capable workers can accelerate large tabular operations and
Dynamo can serve the LLM inference plane. Jetson is treated as an explicit edge
profile, never inferred from a configuration flag alone.

This module deliberately separates four states that are often confused:

- configured: an operator supplied configuration;
- detected: the runtime can prove the hardware/software exists;
- active: Academy selected the component for a request;
- required: failure to use acceleration must fail closed instead of falling back.

That distinction prevents "installed/configured" from being reported as
"operational" without runtime evidence.
"""

from __future__ import annotations

import importlib.util
import logging
import os
import platform
import shutil
import subprocess
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple
from urllib.parse import urlparse

import httpx

logger = logging.getLogger("cvln.nvidia")

DEFAULT_CUDF_MIN_ROWS = 50_000
DEFAULT_DYNAMO_TIMEOUT_SECONDS = 30.0


class NvidiaAccelerationError(RuntimeError):
    """Base error for required NVIDIA acceleration failures."""


class DynamoConfigurationError(NvidiaAccelerationError):
    """Raised when Dynamo is selected without a usable configuration."""


class DynamoUnavailableError(NvidiaAccelerationError):
    """Raised when the configured Dynamo inference endpoint cannot serve a request."""


def _truthy(value: Optional[str]) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _safe_int(value: Optional[str], default: int) -> int:
    try:
        parsed = int(str(value))
    except (TypeError, ValueError):
        return default
    return max(parsed, 0)


def _safe_float(value: Optional[str], default: float) -> float:
    try:
        parsed = float(str(value))
    except (TypeError, ValueError):
        return default
    return max(parsed, 0.1)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore").strip()
    except OSError:
        return ""


def _sanitized_url(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    parsed = urlparse(value)
    if not parsed.scheme or not parsed.netloc:
        return None
    return f"{parsed.scheme}://{parsed.netloc}"


def _nvidia_smi_status() -> Dict[str, Any]:
    executable = shutil.which("nvidia-smi")
    if not executable:
        return {
            "detected": False,
            "driver_version": None,
            "gpus": [],
            "reason": "nvidia-smi-not-found",
        }

    command = [
        executable,
        "--query-gpu=name,driver_version,memory.total",
        "--format=csv,noheader,nounits",
    ]
    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=3,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {
            "detected": False,
            "driver_version": None,
            "gpus": [],
            "reason": f"nvidia-smi-failed:{type(exc).__name__}",
        }

    gpus: List[Dict[str, Any]] = []
    driver_version: Optional[str] = None
    for raw_line in completed.stdout.splitlines():
        parts = [part.strip() for part in raw_line.split(",")]
        if len(parts) < 3:
            continue
        name, driver, memory_mib = parts[:3]
        driver_version = driver_version or driver
        try:
            memory_value: Optional[int] = int(memory_mib)
        except ValueError:
            memory_value = None
        gpus.append(
            {
                "name": name,
                "driver_version": driver,
                "memory_total_mib": memory_value,
            }
        )

    return {
        "detected": bool(gpus),
        "driver_version": driver_version,
        "gpus": gpus,
        "reason": None if gpus else "nvidia-smi-returned-no-gpu",
    }


def _cudf_status() -> Dict[str, Any]:
    if importlib.util.find_spec("cudf") is None:
        return {
            "installed": False,
            "version": None,
            "importable": False,
            "reason": "cudf-not-installed",
        }

    try:
        import cudf  # type: ignore
    except Exception as exc:  # noqa: BLE001 - runtime probe must not crash CPU hosts
        return {
            "installed": True,
            "version": None,
            "importable": False,
            "reason": f"cudf-import-failed:{type(exc).__name__}",
        }

    return {
        "installed": True,
        "version": getattr(cudf, "__version__", None),
        "importable": True,
        "reason": None,
    }


def _jetson_status() -> Dict[str, Any]:
    requested = _truthy(os.environ.get("JETSON_EDGE_MODE"))
    nv_tegra_release = _read_text(Path("/etc/nv_tegra_release"))
    device_model = _read_text(Path("/proc/device-tree/model"))
    detected = bool(nv_tegra_release) or "jetson" in device_model.lower()

    return {
        "requested": requested,
        "detected": detected,
        "device_model": device_model or None,
        "nv_tegra_release": nv_tegra_release or None,
        "active": requested and detected,
        "reason": (
            None
            if detected
            else (
                "edge-mode-requested-but-jetson-not-detected"
                if requested
                else "jetson-not-detected"
            )
        ),
    }


def cuda_runtime_status() -> Dict[str, Any]:
    """Return runtime evidence for CUDA-capable NVIDIA hardware."""
    smi = _nvidia_smi_status()
    required = _truthy(os.environ.get("NVIDIA_ACCELERATION_REQUIRED"))
    return {
        "required": required,
        "detected": smi["detected"],
        "driver_version": smi["driver_version"],
        "gpu_count": len(smi["gpus"]),
        "gpus": smi["gpus"],
        "reason": smi["reason"],
    }


def accelerated_runtime_status() -> Dict[str, Any]:
    """Return non-secret, evidence-based NVIDIA runtime status."""
    cuda = cuda_runtime_status()
    cudf = _cudf_status()
    jetson = _jetson_status()
    dynamo = DynamoClient().status()
    threshold = _safe_int(
        os.environ.get("NVIDIA_CUDF_MIN_ROWS"), DEFAULT_CUDF_MIN_ROWS
    )

    cudf_ready = bool(cuda["detected"] and cudf["importable"])
    return {
        "schema_version": "1.0.0",
        "host": {
            "machine": platform.machine(),
            "system": platform.system(),
            "python": platform.python_version(),
        },
        "cuda": cuda,
        "cudf": {
            **cudf,
            "ready": cudf_ready,
            "min_rows": threshold,
        },
        "dynamo": dynamo,
        "jetson": jetson,
    }


def public_accelerator_status() -> Dict[str, Any]:
    """Coarse status safe for unauthenticated health surfaces."""
    status = accelerated_runtime_status()
    return {
        "cuda_detected": status["cuda"]["detected"],
        "cudf_ready": status["cudf"]["ready"],
        "dynamo_configured": status["dynamo"]["configured"],
        "dynamo_selected": status["dynamo"]["selected"],
        "jetson_detected": status["jetson"]["detected"],
        "jetson_active": status["jetson"]["active"],
    }


def accelerated_group_count(
    records: Iterable[Mapping[str, Any]],
    key: str,
    *,
    min_rows: Optional[int] = None,
    require_gpu: bool = False,
) -> Tuple[Dict[str, int], str, Optional[str]]:
    """Count values using cuDF when it is beneficial and proven available.

    Returns ``(counts, engine, fallback_reason)``. Small workloads intentionally
    stay on CPU because GPU transfer/initialization overhead can be slower than a
    Python Counter. When ``require_gpu`` is true, an unavailable or failing GPU
    path raises instead of silently degrading.
    """
    materialized = list(records)
    threshold = (
        min_rows
        if min_rows is not None
        else _safe_int(os.environ.get("NVIDIA_CUDF_MIN_ROWS"), DEFAULT_CUDF_MIN_ROWS)
    )

    if len(materialized) < threshold and not require_gpu:
        counts = Counter(str(item.get(key, "")) for item in materialized)
        return dict(counts), "python", "below-gpu-threshold"

    cuda = cuda_runtime_status()
    cudf = _cudf_status()
    if not (cuda["detected"] and cudf["importable"]):
        reason = cudf.get("reason") or cuda.get("reason") or "gpu-runtime-unavailable"
        if require_gpu:
            raise NvidiaAccelerationError(str(reason))
        counts = Counter(str(item.get(key, "")) for item in materialized)
        return dict(counts), "python", str(reason)

    try:
        import cudf  # type: ignore

        frame = cudf.DataFrame(materialized)
        series = frame[key].fillna("").astype(str).value_counts()
        result = {str(index): int(value) for index, value in series.to_pandas().items()}
        return result, "cudf", None
    except Exception as exc:  # noqa: BLE001 - optional accelerator must be resilient
        reason = f"cudf-execution-failed:{type(exc).__name__}"
        logger.exception("cuDF execution failed; falling back to CPU")
        if require_gpu:
            raise NvidiaAccelerationError(reason) from exc
        counts = Counter(str(item.get(key, "")) for item in materialized)
        return dict(counts), "python", reason


class DynamoClient:
    """Thin OpenAI-compatible client for a separately operated NVIDIA Dynamo plane."""

    def __init__(self) -> None:
        self.base_url = os.environ.get("NVIDIA_DYNAMO_BASE_URL", "").rstrip("/")
        self.api_key = os.environ.get("NVIDIA_DYNAMO_API_KEY")
        self.model = os.environ.get("NVIDIA_DYNAMO_MODEL", "")
        self.chat_path = os.environ.get(
            "NVIDIA_DYNAMO_CHAT_PATH", "/v1/chat/completions"
        )
        self.timeout_seconds = _safe_float(
            os.environ.get("NVIDIA_DYNAMO_TIMEOUT_SECONDS"),
            DEFAULT_DYNAMO_TIMEOUT_SECONDS,
        )

    def is_configured(self) -> bool:
        return bool(self.base_url and self.model)

    def is_selected(self) -> bool:
        return os.environ.get("ACADEMY_AI_TRANSPORT", "anthropic").lower() == "dynamo"

    def status(self) -> Dict[str, Any]:
        return {
            "configured": self.is_configured(),
            "selected": self.is_selected(),
            "base_url": _sanitized_url(self.base_url),
            "model": self.model or None,
            "timeout_seconds": self.timeout_seconds,
            "openai_compatible": True,
        }

    def _endpoint(self) -> str:
        if not self.base_url or not self.model:
            raise DynamoConfigurationError(
                "NVIDIA_DYNAMO_BASE_URL and NVIDIA_DYNAMO_MODEL are required"
            )
        return f"{self.base_url}/{self.chat_path.lstrip('/')}"

    async def chat_reply(
        self,
        *,
        system_prompt: str,
        session_id: str,
        message: str,
        history: List[Dict[str, str]],
    ) -> str:
        """Execute one chat completion against Dynamo's OpenAI-compatible frontend."""
        messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
        messages.extend(
            {"role": item["role"], "content": item["content"]}
            for item in history[-12:]
            if item.get("role") in {"user", "assistant"} and item.get("content")
        )
        messages.append({"role": "user", "content": message})

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 1024,
        }

        started = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(
                    self._endpoint(), headers=headers, json=payload
                )
                response.raise_for_status()
                data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise DynamoUnavailableError(
                f"Dynamo request failed for session {session_id}: {type(exc).__name__}"
            ) from exc

        elapsed_ms = (time.perf_counter() - started) * 1000
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise DynamoUnavailableError("Dynamo returned an invalid chat response") from exc

        if not isinstance(content, str) or not content.strip():
            raise DynamoUnavailableError("Dynamo returned an empty chat response")

        logger.info("Dynamo chat completed session=%s elapsed_ms=%.1f", session_id, elapsed_ms)
        return content.strip()


nvidia_dynamo = DynamoClient()
