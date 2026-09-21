import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path

if sys.version_info < (3, 10):
    sys.exit(
        f"Python 3.10 or newer is required; found "
        f"{sys.version_info.major}.{sys.version_info.minor}."
    )

REQUIREMENTS_FILE = Path(__file__).parent / "requirements.txt"
SCRIPT_DIR = Path(__file__).resolve().parent
LLAMA_CPP_DIR = SCRIPT_DIR / "tools" / "llama.cpp"


def local_llama_bench_candidates() -> list[Path]:
    """Return common local llama-bench paths for the current platform."""
    executable = "llama-bench.exe" if os.name == "nt" else "llama-bench"
    return [
        SCRIPT_DIR / executable,
        SCRIPT_DIR / "bin" / executable,
        LLAMA_CPP_DIR / "build" / "bin" / executable,
        LLAMA_CPP_DIR / "build" / "bin" / "Release" / executable,
    ]


def llama_bench_has_gpu_backend(llama_bench: Path) -> bool:
    """Return whether llama-bench reports at least one accelerator device."""
    try:
        result = subprocess.run(
            [str(llama_bench), "--list-devices"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0 and "(none)" not in result.stdout


def llama_bench_is_runnable(llama_bench: Path) -> bool:
    """Return whether an existing local executable can run on this system."""
    try:
        result = subprocess.run(
            [str(llama_bench), "--version"],
            capture_output=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0


def nvcc_version() -> tuple[int, int] | None:
    """Return the installed CUDA compiler's major and minor version."""
    try:
        result = subprocess.run(
            ["nvcc", "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    if result.returncode != 0:
        return None
    match = re.search(r"release (\d+)\.(\d+)", result.stdout)
    return (int(match.group(1)), int(match.group(2))) if match else None


def needs_blackwell_cuda_fallback() -> bool:
    """Return whether an old nvcc needs a compatible CUDA architecture."""
    version = nvcc_version()
    if version is None or version >= (12, 8) or not shutil.which("nvidia-smi"):
        return False
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=compute_cap", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    if result.returncode != 0:
        return False
    return any(line.strip().startswith("12.") for line in result.stdout.splitlines())


def build_local_llama_bench() -> str:
    """Clone and build llama.cpp locally, then return llama-bench's path."""
    if not shutil.which("git"):
        sys.exit("Could not install llama-bench automatically: 'git' is not installed.")
    if not shutil.which("cmake"):
        sys.exit("Could not install llama-bench automatically: 'cmake' is not installed.")

    try:
        LLAMA_CPP_DIR.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        sys.exit(f"Cannot write local build files in {SCRIPT_DIR}: {exc}")
    if not LLAMA_CPP_DIR.exists():
        print("Downloading llama.cpp for the local benchmark tool ...")
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", "https://github.com/ggml-org/llama.cpp.git", str(LLAMA_CPP_DIR)],
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            sys.exit(f"Could not download llama.cpp (exit {exc.returncode}).")

    cmake_configure = [
        "cmake", "-S", str(LLAMA_CPP_DIR), "-B", str(LLAMA_CPP_DIR / "build"),
        "-DCMAKE_BUILD_TYPE=Release",
    ]
    if shutil.which("nvcc"):
        cmake_configure.append("-DGGML_CUDA=ON")
        if needs_blackwell_cuda_fallback():
            cmake_configure.append("-DCMAKE_CUDA_ARCHITECTURES=89")
            print(
                "Building local llama-bench with CUDA support "
                "(CUDA Toolkit older than 12.8; using compatible sm_89 code) ..."
            )
        else:
            print("Building local llama-bench with CUDA support ...")
    else:
        print("Building local llama-bench without CUDA support (nvcc not found) ...")
    try:
        configure = subprocess.run(cmake_configure)
        if configure.returncode != 0:
            build_dir = LLAMA_CPP_DIR / "build"
            print("Discarding an incompatible local CMake build cache ...")
            shutil.rmtree(build_dir, ignore_errors=True)
            subprocess.run(cmake_configure, check=True)
        subprocess.run(
            ["cmake", "--build", str(LLAMA_CPP_DIR / "build"), "--config", "Release", "--target", "llama-bench"],
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        sys.exit(f"Could not build llama-bench (exit {exc.returncode}).")

    for candidate in local_llama_bench_candidates():
        if candidate.is_file():
            return str(candidate)
    sys.exit("llama.cpp built successfully, but its llama-bench executable was not found.")


def local_build_needs_cuda_upgrade(candidate: Path) -> bool:
    """Return whether a local automatic build should be rebuilt with CUDA."""
    local_build = LLAMA_CPP_DIR / "build" / "bin" / candidate.name
    return (
        candidate == local_build
        and shutil.which("nvcc") is not None
        and shutil.which("nvidia-smi") is not None
        and not llama_bench_has_gpu_backend(candidate)
    )


def ensure_dependencies() -> None:
    """Install missing third-party packages from requirements.txt, if needed."""
    try:
        import huggingface_hub  # noqa: F401
        import requests  # noqa: F401
        import tqdm  # noqa: F401
        return
    except ImportError:
        pass

    pip_check = subprocess.run(
        [sys.executable, "-m", "pip", "--version"],
        capture_output=True,
        text=True,
    )
    if pip_check.returncode != 0:
        print("Installing pip for the current Python interpreter ...")
        ensure_pip = subprocess.run(
            [sys.executable, "-m", "ensurepip", "--upgrade"],
            capture_output=True,
            text=True,
        )
        if ensure_pip.returncode != 0:
            sys.exit(
                "Python dependencies are missing and pip is unavailable. "
                "Install pip for this Python interpreter, then run "
                f"'{sys.executable} -m pip install -r {REQUIREMENTS_FILE}'."
            )

    print("Installing missing dependencies from requirements.txt ...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        sys.exit(f"Could not install Python dependencies (exit {exc.returncode}).")


ensure_dependencies()

import requests
from huggingface_hub import hf_hub_url
from tqdm.auto import tqdm

# ---------------------------------------------------------------------------
# Models to benchmark.
#
# Model definitions live in `models.json` next to this script. Each entry
# points at a GGUF file hosted on the Hugging Face Hub:
#   - repo_id:  the model repository, e.g. "bartowski/Llama-3.2-3B-Instruct-GGUF"
#   - filename: the specific .gguf file inside that repo (pick a quantization),
#               e.g. "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
#   - label:    a short name used in the summary table.
# ---------------------------------------------------------------------------
MODELS_FILE = Path(__file__).parent / "models.json"

# Directory where GGUF files are cached locally.
MODELS_DIR = Path(__file__).parent / "models"


def load_models(models_file: Path) -> list[dict]:
    """Load the list of models to benchmark from a JSON file."""
    if not models_file.is_file():
        sys.exit(f"Models file not found: {models_file}")
    try:
        with open(models_file, encoding="utf-8") as fh:
            models = json.load(fh)
    except json.JSONDecodeError as exc:
        sys.exit(f"Failed to parse {models_file}: {exc}")

    if not isinstance(models, list) or not models:
        sys.exit(f"{models_file} must contain a non-empty JSON array of models.")

    required = {"label", "repo_id", "filename"}
    for i, model in enumerate(models):
        if not isinstance(model, dict):
            sys.exit(f"Model at index {i} in {models_file} must be an object.")
        missing = required - model.keys()
        if missing:
            sys.exit(f"Model at index {i} in {models_file} is missing keys: {sorted(missing)}")
        invalid = [key for key in required if not isinstance(model[key], str) or not model[key].strip()]
        if invalid:
            sys.exit(f"Model at index {i} in {models_file} has invalid values for: {sorted(invalid)}")
    return models


def resolve_llama_bench(explicit: str | None) -> str:
    """Locate the llama-bench executable.

    Resolution order: explicit --llama-bench arg, LLAMA_BENCH env var, local
    copy, PATH, then an automatic local build.
    """
    candidates = [explicit, os.environ.get("LLAMA_BENCH")]
    for candidate in candidates:
        if not candidate:
            continue
        found = shutil.which(candidate) or (candidate if Path(candidate).is_file() else None)
        if found:
            return found

    for candidate in local_llama_bench_candidates():
        if candidate.is_file():
            local_build = LLAMA_CPP_DIR / "build" / "bin" / candidate.name
            if candidate == local_build and not llama_bench_is_runnable(candidate):
                print("Rebuilding an incompatible local llama-bench for this system ...")
                return build_local_llama_bench()
            if local_build_needs_cuda_upgrade(candidate):
                print("Rebuilding the local CPU-only llama-bench with CUDA support ...")
                return build_local_llama_bench()
            return str(candidate)

    found = shutil.which("llama-bench")
    if found:
        return found
    return build_local_llama_bench()


def download_model(model: dict) -> Path:
    """Download the GGUF file for a model (cached) and return its local path.

    Streams the file directly and renders a single progress bar showing the
    percentage complete and download speed.
    """
    dest_dir = MODELS_DIR / model["label"]
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / model["filename"]

    url = hf_hub_url(repo_id=model["repo_id"], filename=model["filename"])
    headers = {}
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        with requests.get(url, headers=headers, stream=True, timeout=60) as response:
            response.raise_for_status()
            total = int(response.headers.get("Content-Length", 0))

            # Skip re-downloading if the cached file is already complete.
            if dest.exists() and total and dest.stat().st_size == total:
                print(f"[{model['label']}] {model['filename']} already downloaded.")
                return dest

            with open(dest, "wb") as fh, tqdm(
                total=total or None,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc=model["label"],
                leave=True,
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        fh.write(chunk)
                        bar.update(len(chunk))
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        hint = " Set HF_TOKEN to a Hugging Face access token and try again." if status == 429 else ""
        sys.exit(f"Could not download {model['filename']}: HTTP {status}.{hint}")
    except requests.exceptions.RequestException as exc:
        sys.exit(f"Could not download {model['filename']}: {exc}")

    return dest


class GpuMonitor:
    """Samples GPU VRAM usage and utilization in a background thread.

    Uses `nvidia-smi` to poll `memory.used` (MiB) and `utilization.gpu` (%)
    at a fixed interval while a benchmark runs. If `nvidia-smi` is not
    available, monitoring is silently disabled and stats come back empty.
    """

    def __init__(self, gpu_index: int = 0, interval: float = 0.25) -> None:
        self.gpu_index = gpu_index
        self.interval = interval
        self.available = shutil.which("nvidia-smi") is not None
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._mem_samples: list[float] = []
        self._util_samples: list[float] = []
        self.baseline_vram_mib: float | None = None

    @staticmethod
    def _query(gpu_index: int, interval: float) -> tuple[float, float] | None:
        """Return a single (memory.used MiB, utilization %) sample, or None."""
        try:
            output = subprocess.run(
                [
                    "nvidia-smi",
                    f"--id={gpu_index}",
                    "--query-gpu=memory.used,utilization.gpu",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True,
                text=True,
                timeout=interval + 2,
            )
        except (subprocess.SubprocessError, OSError):
            return None
        if output.returncode != 0:
            return None
        line = output.stdout.strip().splitlines()
        if not line:
            return None
        try:
            mem_str, util_str = (part.strip() for part in line[0].split(","))
            return float(mem_str), float(util_str)
        except ValueError:
            return None

    def sample_baseline(self) -> None:
        """Record current VRAM usage as the pre-load baseline."""
        if not self.available:
            return
        sample = self._query(self.gpu_index, self.interval)
        if sample is not None:
            self.baseline_vram_mib = sample[0]

    def _sample_once(self) -> None:
        sample = self._query(self.gpu_index, self.interval)
        if sample is not None:
            self._mem_samples.append(sample[0])
            self._util_samples.append(sample[1])

    def _loop(self) -> None:
        while not self._stop.is_set():
            self._sample_once()
            self._stop.wait(self.interval)

    def __enter__(self) -> "GpuMonitor":
        if self.available:
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()
        return self

    def __exit__(self, *exc) -> None:
        if self._thread is not None:
            self._stop.set()
            self._thread.join()

    def stats(self) -> dict:
        """Return VRAM (peak, baseline, effective) and GPU utilization (%)."""
        if not self._mem_samples:
            return {
                "peak_vram_mib": None,
                "baseline_vram_mib": self.baseline_vram_mib,
                "effective_vram_mib": None,
                "avg_util": None,
                "peak_util": None,
            }
        peak = max(self._mem_samples)
        effective = None
        if self.baseline_vram_mib is not None:
            effective = max(peak - self.baseline_vram_mib, 0.0)
        return {
            "peak_vram_mib": peak,
            "baseline_vram_mib": self.baseline_vram_mib,
            "effective_vram_mib": effective,
            "avg_util": sum(self._util_samples) / len(self._util_samples),
            "peak_util": max(self._util_samples),
        }


def run_llama_bench(llama_bench: str, model_path: Path, args) -> tuple[list[dict], dict]:
    """Run llama-bench on a single model.

    Returns the parsed JSON rows and a dict of GPU stats captured while the
    benchmark ran (peak VRAM and GPU utilization).
    """
    cmd = [
        llama_bench,
        "-m", str(model_path),
        "-p", str(args.prompt),
        "-n", str(args.generate),
        "-pg", f"{args.prompt},{args.generate}",
        "-ngl", str(args.gpu_layers),
        "-r", str(args.repeats),
        "-o", "json",
    ]
    print(f"  running: {' '.join(cmd)}")
    monitor = GpuMonitor(gpu_index=args.gpu_index)
    # Capture idle VRAM before the model loads so we can report the model's
    # effective usage (peak during benchmark minus this baseline).
    monitor.sample_baseline()
    with monitor:
        result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(f"llama-bench failed for {model_path.name} (exit {result.returncode})")
    return json.loads(result.stdout), monitor.stats()


def summarize(results: list[dict]) -> None:
    """Print a comparison table with one column per test (t/s per model)."""
    if not results:
        print("No results to summarize.")
        return

    # Collect the set of test labels across all models, preserving order.
    test_labels: list[str] = []
    for entry in results:
        for row in entry["rows"]:
            test = f"{row.get('n_prompt', 0)}+{row.get('n_gen', 0)}"
            if test not in test_labels:
                test_labels.append(test)

    # Build the header: model column followed by one column per test.
    col_width = 11
    header = f"{'model':<20}" + "".join(f"{test:>{col_width}}" for test in test_labels)
    print("\n" + header)
    print("-" * len(header))

    for entry in results:
        tps_by_test = {
            f"{row.get('n_prompt', 0)}+{row.get('n_gen', 0)}": row.get("avg_ts", 0.0)
            for row in entry["rows"]
        }
        line = f"{entry['label']:<20}"
        for test in test_labels:
            value = tps_by_test.get(test)
            line += f"{value:>{col_width}.2f}" if value is not None else f"{'-':>{col_width}}"
        print(line)

    _summarize_gpu(results)


def _summarize_gpu(results: list[dict]) -> None:
    """Print per-model GPU VRAM and utilization captured during the run."""
    if not any(entry.get("gpu", {}).get("peak_vram_mib") is not None for entry in results):
        print("\n(GPU stats unavailable - nvidia-smi not found or no samples.)")
        return

    header = (
        f"{'model':<20}{'base GiB':>10}{'peak GiB':>10}"
        f"{'model GiB':>11}{'avg %':>8}{'peak %':>8}"
    )
    print("\n" + header)
    print("-" * len(header))
    for entry in results:
        gpu = entry.get("gpu", {})
        baseline = gpu.get("baseline_vram_mib")
        vram = gpu.get("peak_vram_mib")
        effective = gpu.get("effective_vram_mib")
        avg_util = gpu.get("avg_util")
        peak_util = gpu.get("peak_util")
        line = f"{entry['label']:<20}"
        line += f"{baseline / 1024:>10.2f}" if baseline is not None else f"{'-':>10}"
        line += f"{vram / 1024:>10.2f}" if vram is not None else f"{'-':>10}"
        line += f"{effective / 1024:>11.2f}" if effective is not None else f"{'-':>11}"
        line += f"{avg_util:>8.1f}" if avg_util is not None else f"{'-':>8}"
        line += f"{peak_util:>8.1f}" if peak_util is not None else f"{'-':>8}"
        print(line)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download GGUF models and benchmark them with llama-bench."
    )
    parser.add_argument("--llama-bench", help="Path to the llama-bench executable.")
    parser.add_argument("-p", "--prompt", type=int, default=512,
                        help="Prompt (prefill) size in tokens.")
    parser.add_argument("-n", "--generate", type=int, default=128,
                        help="Number of tokens to generate (decode).")
    parser.add_argument("-ngl", "--gpu-layers", type=int, default=99,
                        help="Number of layers to offload to the GPU.")
    parser.add_argument("-r", "--repeats", type=int, default=3,
                        help="Repetitions per test for averaging.")
    parser.add_argument("--gpu-index", type=int, default=0,
                        help="GPU index to monitor with nvidia-smi for VRAM/utilization.")
    parser.add_argument("--models-file", type=Path, default=MODELS_FILE,
                        help="Path to the JSON file listing models to benchmark.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    models = load_models(args.models_file)

    llama_bench = resolve_llama_bench(args.llama_bench)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    for model in models:
        model_path = download_model(model)
        rows, gpu_stats = run_llama_bench(llama_bench, model_path, args)
        results.append({"label": model["label"], "rows": rows, "gpu": gpu_stats})

    summarize(results)


if __name__ == "__main__":
    main()
