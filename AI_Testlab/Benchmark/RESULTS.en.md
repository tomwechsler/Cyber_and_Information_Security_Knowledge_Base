# Interpreting Benchmark Results

*[Deutsche Version siehe RESULTS.md](RESULTS.md)*

This file explains how to read the tables printed by `main.py`. See
[PURPOSE.en.md](PURPOSE.en.md) for what the script does, and
[README.md](README.md) for installation instructions.

## Example output

```text
model                     512+0       0+64     512+64
-----------------------------------------------------
gemma-4-e4b-q4_k_m      2463.19      52.08     396.67
qwen-3.5-4b-q4_k_m      2171.62      56.50     421.05
llama-3.2-3b-q4_k_m     4026.60      83.98     633.19

model                 base GiB  peak GiB  model GiB   avg %  peak %
-------------------------------------------------------------------
gemma-4-e4b-q4_k_m        0.63      4.10       3.47    79.7   100.0
qwen-3.5-4b-q4_k_m        0.57      3.82       3.24    82.6   100.0
llama-3.2-3b-q4_k_m       0.61      2.91       2.29    64.7    99.0
```

## Table 1: Throughput (tokens/second)

Each column represents a `prompt+generate` test configuration (in tokens):

- **`512+0`** — pure **prompt processing (prefill)**: how fast the model
  reads/processes a 512-token prompt before generation starts. High numbers
  here are normal since prefill is highly parallelizable (many tokens at
  once).
- **`0+64`** — pure **text generation (decode)**: how many new tokens per
  second are produced starting from an empty/short prompt. This is usually
  the most meaningful number for "how fast chatting feels", since decode
  happens token-by-token (sequentially) and is therefore much slower than
  prefill.
- **`512+64`** — a **combined, more realistic request**: a 512-token prompt
  followed by 64 generated tokens. Throughput naturally falls between the two
  extremes.

**How to compare models:**
- Higher values = faster.
- For "how fast a chat feels", look at the `0+n` column (decode).
- For "how fast large contexts/documents are processed", look at the `p+0`
  column (prefill).
- Model size and quantization (`Q4_K_M`, `Q6_K`, …) strongly affect
  throughput: smaller/more aggressively quantized models are usually faster
  but potentially less accurate (this tool does **not** measure accuracy).

## Table 2: GPU metrics

- **`base GiB`** — VRAM usage *before* the model was loaded (baseline, e.g.
  occupied by the desktop environment or other processes).
- **`peak GiB`** — maximum VRAM usage *during* the entire benchmark run
  (model weights + runtime buffers such as the KV cache).
- **`model GiB`** — the model's effective VRAM footprint
  (`peak GiB - base GiB`). This is the relevant number for estimating whether
  a model fits on the monitored GPU. When multiple GPUs are visible, llama.cpp
  can distribute model layers, so this value covers only `--gpu-index`, not
  the total allocation across all GPUs.
- **`avg %` / `peak %`** — average and maximum GPU utilization (compute, not
  memory) during the benchmark. Values close to 100% indicate the GPU is the
  limiting factor (well utilized). Low values (e.g. < 30%) suggest another
  bottleneck — such as CPU overhead, insufficient GPU offloading (`-ngl`), or
  a CPU-only `llama-bench` build without CUDA/Metal/ROCm support.

If the GPU table shows `(GPU stats unavailable - nvidia-smi not found or no
samples.)`, either no NVIDIA GPU is present or `nvidia-smi` is not on `PATH`.

## Common interpretation pitfalls

- **CPU vs. GPU build**: If `llama-bench` was built without `-DGGML_CUDA=ON`
  (or an equivalent backend), inference runs entirely on the CPU — even if a
  GPU is present. This shows up as very low `avg %`/`peak %` (or `0.0`)
  despite having a GPU. See [README.md](README.md) for the GPU build.
- **`-ngl` (GPU layers)**: If this value is too low, only a few model layers
  are offloaded to the GPU and the rest runs on the CPU — this lowers both
  throughput and GPU utilization.
- **Multiple GPUs**: `llama-bench` uses automatic device selection by default
  and can distribute layers. The script monitors only the GPU selected by
  `--gpu-index`. For unambiguous VRAM measurements, limit the process to one
  GPU, for example: `CUDA_VISIBLE_DEVICES=0 python main.py --gpu-index 0`.
- **One GPU**: With one visible NVIDIA GPU, `-ngl 99` and `--gpu-index 0` are
  the appropriate defaults. If its VRAM is insufficient, reduce `-ngl` or use
  `-ngl 0` for CPU execution.
- **Repeats (`-r`)**: The displayed values are already averaged over `-r`
  repetitions. A higher repeat count gives more stable but slower-to-obtain
  results.
- **Results are hardware-specific**: Absolute numbers are only meaningfully
  comparable between models run on the **same** machine, not across
  different hardware.
