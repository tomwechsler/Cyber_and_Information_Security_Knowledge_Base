# Task-Eval

*[Deutsche Version siehe README.de.md](README.de.md)*

A small evaluation harness that classifies support tickets with local
Ollama models, compares their accuracy, and reports performance, memory,
and GPU usage.

The script ([main.py](main.py)) runs each model against random samples of
labeled tickets from [eval-cases.json](eval-cases.json) and prints a
comparison summary.

See [PURPOSE.en.md](PURPOSE.en.md) for a detailed explanation of what
`main.py` does internally, and [RESULTS.en.md](RESULTS.en.md) for how to
interpret the printed tables.

## Prerequisites

- **Ollama** — runs the local models.
- **Python 3.10+**

`main.py` is self-contained: on every run it automatically installs any
missing Python dependencies (from `requirements.txt`), checks that the
Ollama server is reachable, and pulls any of the required models
(`llama3.2:3b`, `qwen3.5:4b`) that are not yet available locally. The only
manual prerequisite is installing and starting Ollama itself.

- **NVIDIA GPU (optional)** — the GPU usage table (utilization, power draw,
  memory) is collected via `nvidia-smi` and therefore requires an NVIDIA card
  with drivers installed. On machines without `nvidia-smi`, the script still
  runs; the GPU section simply reports "nvidia-smi unavailable / no samples".

## 1. Install Ollama

Download and install from https://ollama.com/download, then verify it is
running:

```bash
ollama --version
```

Start the Ollama app/service so its API is reachable at
`http://localhost:11434`. `main.py` will refuse to run with a clear error
message if it cannot reach this URL.

## 2. Set up the Python environment (optional)

`main.py` installs its own missing Python dependencies (from
`requirements.txt`) the first time it is run, so a manual `pip install` step
is optional. If you still want to prepare the environment up front, from the
repository root:

```bash
uv venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\Activate.ps1
uv pip install -r Task-Eval/requirements.txt
```

## 3. Run the evaluation

```bash
cd Task-Eval
python3 main.py
```

On Windows, use `py main.py` instead of `python3 main.py`. If only this
directory was copied, change into it first and run the same command there.

The first run automatically pulls any missing models
(`ollama pull llama3.2:3b`, `ollama pull qwen3.5:4b`) — no manual `ollama
pull` step required. By default this samples 10 cases per run, repeats 3
times per model, and shows a progress bar followed by a comparison summary.

### Command-line options

| Argument | Default | Description |
| --- | --- | --- |
| `-n`, `--sample-size` | `10` | Number of cases randomly sampled per run. |
| `-x`, `--repeats` | `3` | Number of runs, each with a fresh random sample. |
| `--show-cases` | off | Print each ticket/expected/result instead of a progress bar. |
| `-h`, `--help` | — | Show help and exit. |

Examples:

```bash
# Larger evaluation: 20 cases, 5 runs
python3 Task-Eval/main.py -n 20 -x 5

# Show each case as it is processed
python3 Task-Eval/main.py --show-cases
```

### Optional: `start-models.sh` / `start-models.ps1`

[start-models.sh](start-models.sh) and [start-models.ps1](start-models.ps1)
are convenience wrappers that set up the `uv` environment and run `main.py`
in one step. They are no longer required (since `main.py` now handles
dependency and model setup itself) but are kept for those who prefer an
all-in-one script.

## Output

The script prints two tables:

- **Model comparison summary** — category / urgency / exact-match accuracy,
  throughput (tokens/sec), average latency, and model memory / VRAM footprint
  (from Ollama's `/api/ps` endpoint).
- **GPU usage** — average and peak GPU utilization, power draw, and peak GPU
  memory sampled from `nvidia-smi` during each model's run. **Requires an
  NVIDIA GPU.**

Each model is loaded on demand and unloaded after its run so the statistics
are isolated per model.

