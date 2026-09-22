import argparse
import json
import random
import shutil
import subprocess
import sys
import threading
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_FILE = SCRIPT_DIR / "requirements.txt"


def ensure_dependencies() -> None:
    """Install missing third-party packages from requirements.txt, if needed."""
    try:
        import requests  # noqa: F401
        import tqdm  # noqa: F401
        return
    except ImportError:
        pass

    print("Installing missing dependencies from requirements.txt ...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
        check=True,
    )


ensure_dependencies()

import requests
from tqdm import tqdm

MODELS = ["llama3.2:3b", "qwen3.5:4b"]

OLLAMA_URL = "http://localhost:11434"


def ensure_ollama_running() -> None:
    """Verify the local Ollama server is reachable, or exit with instructions."""
    try:
        requests.get(f"{OLLAMA_URL}/api/version", timeout=5).raise_for_status()
    except requests.RequestException:
        sys.exit(
            "Could not reach Ollama at "
            f"{OLLAMA_URL}. Install it from https://ollama.com/download and make "
            "sure the Ollama app/service is running, then try again."
        )


def ensure_models_pulled(models: list[str]) -> None:
    """Pull any of the given Ollama models that are not already available locally."""
    response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=30)
    response.raise_for_status()
    available = {m["name"] for m in response.json().get("models", [])}

    missing = [model for model in models if model not in available]
    if missing and shutil.which("ollama") is None:
        sys.exit(
            "The Ollama API is reachable, but the 'ollama' command was not found. "
            "Install Ollama and ensure its command is available on PATH, then try again."
        )

    for model in missing:
        print(f"Model '{model}' not found locally, pulling with 'ollama pull {model}' ...")
        subprocess.run(["ollama", "pull", model], check=True)

SCHEMA = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": ["billing", "technical", "account", "security", "feature_request"]
        },
        "urgency": {
            "type": "string",
            "enum": ["low", "medium", "high"]
        },
        "reason": {
            "type": "string"
        }
    },
    "required": ["category", "urgency", "reason"]
}

with open(SCRIPT_DIR / "eval-cases.json", encoding="utf-8") as f:
    EVAL_CASES = json.load(f)

def call_ollama(model, ticket):
    prompt = f"""
Classify this support ticket.

Ticket:
{ticket}

Return only JSON matching the schema.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "format": SCHEMA,
            "options": {
                "temperature": 0
            }
        },
        timeout=120
    )

    response.raise_for_status()
    data = response.json()
    return json.loads(data["response"]), data


def get_memory_usage(model):
    """Return (total_bytes, vram_bytes) for a currently loaded model, or (0, 0)."""
    response = requests.get("http://localhost:11434/api/ps", timeout=30)
    response.raise_for_status()
    for m in response.json().get("models", []):
        if m.get("name") == model or m.get("model") == model:
            return m.get("size", 0), m.get("size_vram", 0)
    return 0, 0


def load_model(model):
    """Load a model into memory (empty prompt) so it is resident before timing."""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "keep_alive": "5m"},
        timeout=120,
    )
    response.raise_for_status()


def unload_model(model):
    """Unload a model from memory by setting keep_alive to 0."""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "keep_alive": 0},
        timeout=120,
    )
    response.raise_for_status()


class GpuMonitor:
    """Poll nvidia-smi in a background thread and collect GPU utilization stats."""

    def __init__(self, interval=0.25):
        self.interval = interval
        self.available = shutil.which("nvidia-smi") is not None
        self.util_samples = []
        self.mem_samples = []
        self.power_samples = []
        self._stop = threading.Event()
        self._thread = None

    def _sample(self):
        while not self._stop.is_set():
            try:
                out = subprocess.check_output(
                    [
                        "nvidia-smi",
                        "--query-gpu=utilization.gpu,memory.used,power.draw",
                        "--format=csv,noheader,nounits",
                    ],
                    text=True,
                    timeout=self.interval + 2,
                )
                util, mem, power = (p.strip() for p in out.strip().split(","))
                self.util_samples.append(float(util))
                self.mem_samples.append(float(mem))
                self.power_samples.append(float(power))
            except (subprocess.SubprocessError, ValueError):
                pass
            self._stop.wait(self.interval)

    def __enter__(self):
        if self.available:
            self._thread = threading.Thread(target=self._sample, daemon=True)
            self._thread.start()
        return self

    def __exit__(self, *exc):
        self._stop.set()
        if self._thread is not None:
            self._thread.join()

    def stats(self):
        def summarize(samples):
            if not samples:
                return 0.0, 0.0
            return sum(samples) / len(samples), max(samples)

        avg_util, peak_util = summarize(self.util_samples)
        _, peak_mem = summarize(self.mem_samples)
        avg_power, peak_power = summarize(self.power_samples)
        return {
            "gpu_avg_util": avg_util,
            "gpu_peak_util": peak_util,
            "gpu_peak_mem_mb": peak_mem,
            "gpu_avg_power_w": avg_power,
            "gpu_peak_power_w": peak_power,
        }


def evaluate(model, sample_size, repeats, show_cases=False):
    category_correct = 0
    urgency_correct = 0
    exact_correct = 0
    total_eval_tokens = 0
    total_eval_duration = 0
    total_duration = 0

    n = min(sample_size, len(EVAL_CASES))
    total_cases = n * repeats

    print(f"\nEvaluating {model} ({repeats} runs x {n} cases)")
    print("-" * 40)

    load_model(model)

    progress = None if show_cases else tqdm(total=total_cases, desc=model, unit="case")
    with GpuMonitor() as gpu:
        for run in range(1, repeats + 1):
            sample = random.sample(EVAL_CASES, n)
            if show_cases:
                print(f"\n--- Run {run}/{repeats} ---")
            for case in sample:
                result, meta = call_ollama(model, case["ticket"])

                category_ok = result["category"] == case["category"]
                urgency_ok = result["urgency"] == case["urgency"]
                exact_ok = category_ok and urgency_ok

                category_correct += category_ok
                urgency_correct += urgency_ok
                exact_correct += exact_ok

                total_eval_tokens += meta.get("eval_count", 0)
                total_eval_duration += meta.get("eval_duration", 0)
                total_duration += meta.get("total_duration", 0)

                if show_cases:
                    print(f"Ticket: {case['ticket']}")
                    print(f"Expected: {case['category']} / {case['urgency']}")
                    print(f"Got:      {result['category']} / {result['urgency']}")
                    print(f"Reason:   {result['reason']}")
                    print()
                else:
                    progress.update(1)

    if progress is not None:
        progress.close()

    gpu_stats = gpu.stats()
    size_bytes, vram_bytes = get_memory_usage(model)

    unload_model(model)

    total = total_cases
    tokens_per_sec = (
        total_eval_tokens / (total_eval_duration / 1e9)
        if total_eval_duration else 0
    )
    return {
        "model": model,
        "category_accuracy": category_correct / total,
        "urgency_accuracy": urgency_correct / total,
        "exact_match": exact_correct / total,
        "tokens_per_sec": tokens_per_sec,
        "avg_latency_s": (total_duration / total) / 1e9 if total else 0,
        "memory_mb": size_bytes / 1e6,
        "vram_mb": vram_bytes / 1e6,
        **gpu_stats,
    }


def print_summary(results):
    print("\n" + "=" * 96)
    print("MODEL COMPARISON SUMMARY")
    print("=" * 96)
    header = (
        f"{'Model':<16}{'Category':>9}{'Urgency':>9}{'Exact':>8}"
        f"{'Tok/s':>9}{'Latency(s)':>12}{'Memory(MB)':>12}{'VRAM(MB)':>11}"
    )
    print(header)
    print("-" * 96)
    for r in results:
        gpu_pct = (r["vram_mb"] / r["memory_mb"] * 100) if r["memory_mb"] else 0
        print(
            f"{r['model']:<16}"
            f"{r['category_accuracy']:>9.0%}"
            f"{r['urgency_accuracy']:>9.0%}"
            f"{r['exact_match']:>8.0%}"
            f"{r['tokens_per_sec']:>9.1f}"
            f"{r['avg_latency_s']:>12.2f}"
            f"{r['memory_mb']:>12.0f}"
            f"{r['vram_mb']:>8.0f} ({gpu_pct:.0f}%)"
        )
    print("=" * 96)

    print("\nGPU USAGE (nvidia-smi, sampled during each run)")
    print("=" * 96)
    gpu_header = (
        f"{'Model':<16}{'Avg Util%':>10}{'Peak Util%':>11}"
        f"{'Avg Power(W)':>14}{'Peak Power(W)':>15}{'Peak Mem(MB)':>14}"
    )
    print(gpu_header)
    print("-" * 96)
    for r in results:
        if not r.get("gpu_peak_util") and not r.get("gpu_avg_util"):
            print(f"{r['model']:<16}{'nvidia-smi unavailable / no samples':>60}")
            continue
        print(
            f"{r['model']:<16}"
            f"{r['gpu_avg_util']:>10.1f}"
            f"{r['gpu_peak_util']:>11.1f}"
            f"{r['gpu_avg_power_w']:>14.1f}"
            f"{r['gpu_peak_power_w']:>15.1f}"
            f"{r['gpu_peak_mem_mb']:>14.0f}"
        )
    print("=" * 96)


def main():
    def positive_int(value):
        parsed = int(value)
        if parsed < 1:
            raise argparse.ArgumentTypeError("must be a positive integer")
        return parsed

    parser = argparse.ArgumentParser(description="Evaluate and compare Ollama models.")
    parser.add_argument(
        "--show-cases",
        action="store_true",
        help="Print each eval case as it is processed instead of a progress bar.",
    )
    parser.add_argument(
        "-n",
        "--sample-size",
        type=positive_int,
        default=10,
        help="Number of cases to randomly sample per run (default: 10).",
    )
    parser.add_argument(
        "-x",
        "--repeats",
        type=positive_int,
        default=3,
        help="Number of runs, each with a new random sample (default: 3).",
    )
    args = parser.parse_args()

    ensure_ollama_running()
    ensure_models_pulled(MODELS)

    results = [
        evaluate(model, args.sample_size, args.repeats, show_cases=args.show_cases)
        for model in MODELS
    ]
    print_summary(results)


if __name__ == "__main__":
    main()