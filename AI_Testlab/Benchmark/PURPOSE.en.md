# Purpose of `main.py`

*[Deutsche Version siehe PURPOSE.md](PURPOSE.md)*

`main.py` is a benchmarking tool that measures and compares the raw inference
speed (not accuracy) of different local LLMs in GGUF format.

## What the script does in detail

1. **Ensure dependencies**: On startup, `ensure_dependencies()` checks
   whether `requests`, `huggingface_hub`, and `tqdm` are importable. If not,
   they are automatically installed via `pip install -r requirements.txt`.
2. **Load the model list**: `load_models()` reads `models.json`. Each model
   definition contains `label` (short name), `repo_id` (Hugging Face repo),
   and `filename` (the specific `.gguf` file/quantization).
3. **Resolve `llama-bench`**: `resolve_llama_bench()` locates the
   `llama-bench` executable (from llama.cpp) via `--llama-bench`, the
   `LLAMA_BENCH` environment variable, local directories, or the `PATH`. If
   none is available, it clones and builds llama.cpp under `tools/llama.cpp/`.
   CUDA is enabled automatically when `nvcc` is available.
4. **Download models**: `download_model()` downloads the matching GGUF file
   from Hugging Face for each model (with a progress bar) and caches it under
   `Benchmark/models/<label>/`. Already-complete downloads are not re-fetched.
5. **Monitor the GPU**: The `GpuMonitor` class samples VRAM usage and GPU
   utilization in the background via `nvidia-smi` (a baseline before the
   model loads, plus peak values during the benchmark).
6. **Run the benchmark**: `run_llama_bench()` invokes `llama-bench` with the
   chosen parameters (prompt/generation length, GPU layers, repeats) for each
   model and parses the JSON results.
7. **Summarize results**: `summarize()` prints a comparison table with
   tokens/second per model and test configuration (`prompt+generate`), plus a
   second table with GPU metrics (baseline/peak VRAM in GiB, effective model
   VRAM footprint, average/peak GPU utilization).

## In short

The script automates the full workflow of "download model → run benchmark
with llama-bench → measure throughput and GPU resource usage → compare
results in a table," to objectively compare different GGUF models in terms
of speed and resource consumption.
