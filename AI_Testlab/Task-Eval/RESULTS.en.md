# Interpreting Evaluation Results

*[Deutsche Version siehe RESULTS.md](RESULTS.md)*

This file explains how to read the tables printed by `main.py`. See
[PURPOSE.en.md](PURPOSE.en.md) for what the script does, and
[README.md](README.md) for installation instructions.

## Example output

```text
================================================================================================
MODEL COMPARISON SUMMARY
================================================================================================
Model            Category  Urgency   Exact    Tok/s  Latency(s)  Memory(MB)   VRAM(MB)
------------------------------------------------------------------------------------------------
llama3.2:3b           90%       80%      75%     45.2        1.24        2145     2050 (96%)
qwen3.5:4b             95%       85%      85%     38.7        1.58        2890     2780 (96%)
================================================================================================

GPU USAGE (nvidia-smi, sampled during each run)
================================================================================================
Model            Avg Util%  Peak Util%  Avg Power(W)  Peak Power(W)  Peak Mem(MB)
------------------------------------------------------------------------------------------------
llama3.2:3b            62.3        98.0          45.1           68.2          2312
qwen3.5:4b             71.5        99.0          52.4           74.8          3050
================================================================================================
```

## Table 1: Model comparison summary

- **`Category`** — fraction of cases where the model's returned ticket
  **category** (`billing`, `technical`, `account`, `security`,
  `feature_request`) matches the expected category.
- **`Urgency`** — fraction of cases where the returned **urgency**
  (`low`, `medium`, `high`) is correct.
- **`Exact`** — fraction of cases where **both** category **and** urgency
  are correct (the strictest accuracy figure).
- **`Tok/s`** — text-generation throughput (tokens/second), computed from
  Ollama's `eval_count`/`eval_duration`. Higher = faster.
- **`Latency(s)`** — average end-to-end response time per request
  (including prompt processing), in seconds. Lower = faster.
- **`Memory(MB)`** — total size of the loaded model as reported by Ollama
  (`/api/ps`, field `size`).
- **`VRAM(MB)` `(x%)`** — the portion of the model actually residing in GPU
  memory (field `size_vram`), and the percentage `VRAM / Memory`. A value
  close to 100% means the model runs entirely on the GPU; a lower value
  indicates partial CPU offloading (e.g. because the model doesn't fully fit
  in VRAM).

**How to compare models:**
- For **task quality**: compare `Category`, `Urgency`, and especially
  `Exact` — higher is better.
- For **speed**: compare `Tok/s` (higher is better) and `Latency(s)` (lower
  is better).
- There is often a trade-off: larger models (more `Memory(MB)`) tend to be
  more accurate but slower (lower `Tok/s`, higher `Latency(s)`).
- The number of sampled cases (`-n`) and repeats (`-x`) affects how
  stable/meaningful the percentages are — with small `-n` values, a single
  misclassification can shift the percentage significantly.

## Table 2: GPU usage

- **`Avg Util%` / `Peak Util%`** — average and maximum GPU utilization
  (compute) during the model's run. Values close to 100% indicate the GPU is
  the limiting factor.
- **`Avg Power(W)` / `Peak Power(W)`** — average and maximum GPU power draw
  in watts during the run — a rough indicator of energy consumption/
  efficiency.
- **`Peak Mem(MB)`** — maximum GPU memory usage (whole system, not just this
  model) during the run.

If this table shows `nvidia-smi unavailable / no samples`, either no NVIDIA
GPU is present or `nvidia-smi` is not on `PATH`.

## Common interpretation pitfalls

- **Small samples are noisy**: With `-n 10`, a single misclassified case can
  shift accuracy by 10 percentage points. For more reliable numbers, increase
  `-n` and/or `-x`. Since both scripts use identical test material for all
  models, comparisons between models remain fair regardless.
- **Results are hardware- and model-version-specific**: Absolute numbers
  (especially `Tok/s`, `Latency`, GPU figures) are only meaningfully
  comparable between models run on the **same** machine.
- **`temperature: 0`**: The script calls Ollama with `temperature=0`
  (deterministic), so repeated runs on the same tickets should produce the
  same classification results — variation between repeats (`-x`) comes
  primarily from the random selection of different ticket samples, not from
  model randomness.
- **VRAM percentage < 100%**: May indicate the model is partially running on
  the CPU (slower) — typically relevant for large models on GPUs with
  limited memory.
