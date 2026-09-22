# Purpose of `main.py`

*[Deutsche Version siehe PURPOSE.md](PURPOSE.md)*

`main.py` is an evaluation tool that measures and compares the
**classification accuracy** (not raw speed) of different local Ollama
models on a concrete task: classifying support tickets.

## What the script does in detail

1. **Ensure dependencies**: On startup, `ensure_dependencies()` checks
   whether `requests` and `tqdm` are importable. If not, they are
   automatically installed via `pip install -r requirements.txt`.
2. **Check the Ollama server**: `ensure_ollama_running()` checks whether the
   Ollama API is reachable at `http://localhost:11434`. If not, the script
   exits with a clear error message.
3. **Ensure models are available**: `ensure_models_pulled()` queries the
   list of locally available models (`/api/tags`) and automatically pulls
   any missing models from `MODELS` (`llama3.2:3b`, `qwen3.5:4b`) via
   `ollama pull <model>`.
4. **Load test cases**: On import, [eval-cases.json](eval-cases.json) is
   read — a list of support tickets with an expected `category` and
   `urgency`.
5. **Load model & measure memory**: For each model, it is first loaded into
   Ollama's memory via `load_model()` so the subsequent timing is not
   skewed by the load itself.
6. **Monitor the GPU**: The `GpuMonitor` class samples GPU utilization,
   memory usage, and power draw in the background via `nvidia-smi`.
7. **Evaluate**: `evaluate()` draws a random sample (`-n`/`--sample-size`)
   from the test cases for each repeat (`-x`/`--repeats`), calls
   `call_ollama()` for every ticket (the model must return structured JSON
   matching `SCHEMA` with `category`, `urgency`, and `reason`), and compares
   the result against the expected category/urgency.
8. **Collect metrics**: From the Ollama responses, it computes accuracy
   (category, urgency, exact match), tokens/second, average latency, and
   memory/VRAM footprint (`/api/ps`).
9. **Unload the model**: After evaluation, the model is removed from memory
   via `unload_model()` so that measurements for different models don't
   influence each other.
10. **Summarize results**: `print_summary()` prints two tables: a comparison
    summary (accuracy, throughput, latency, memory) and a GPU usage table
    (utilization, power draw, peak memory).

## In short

The script automates the full workflow of "load model → classify random
ticket samples → measure accuracy and performance → unload model → compare
results in a table," to objectively compare different Ollama models in terms
of classification quality, speed, and resource consumption on the same task.
