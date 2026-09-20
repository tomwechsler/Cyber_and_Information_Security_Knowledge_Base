# Benchmark

*[Deutsche Version siehe README.de.md](README.de.md)*

Downloads GGUF model files from the Hugging Face Hub and measures
their raw inference throughput with `llama-bench` (from llama.cpp).

Unlike `Task-Eval`, this harness does **not** test accuracy — it reports
prompt-processing (prefill) and text-generation (decode) speed in tokens/sec.

See [PURPOSE.en.md](PURPOSE.en.md) for a detailed explanation of what
`main.py` does internally.

## Prerequisites

- **Python 3.10+**
- **cmake**, a C/C++ compiler (`gcc`/`g++`), and `git` — required to build
  llama.cpp from source on the first run.
- **Internet access** — required on the first run to clone llama.cpp and
  download the selected models from Hugging Face.
- **Disk space** — allow roughly 15 GiB for the included models and the local
  llama.cpp build; exact usage depends on the models in `models.json`.
- (Optional) **NVIDIA GPU + CUDA Toolkit** — to benchmark with GPU
  offloading instead of CPU-only inference.

## 1. Install build tools

### Linux (Debian/Ubuntu)

```bash
sudo apt-get update
sudo apt-get install -y cmake gcc g++ git
```

### Windows

Install [CMake](https://cmake.org/download/), [Git](https://git-scm.com/),
and a C++ toolchain (e.g. Visual Studio Build Tools with the "Desktop
development with C++" workload).

## 2. (Optional) Install the CUDA Toolkit for GPU support

Skip this step if you only want to benchmark on CPU.

### Linux (Debian/Ubuntu)

```bash
sudo apt-get install -y nvidia-cuda-toolkit
```

Verify with:

```bash
nvcc --version
nvidia-smi
```

### Windows

Install the [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads).

## 3. Automatic `llama-bench` setup

When no executable is supplied, `main.py` clones llama.cpp and builds
`llama-bench` automatically in `Benchmark/tools/llama.cpp/` on its first
run. This means the `Benchmark` folder can be copied to another system and
run without installing llama.cpp or modifying `PATH`; `git`, `cmake`, and a
C++ compiler are still required. The compiled executable is reused on later
runs. When `nvcc` is available, the automatic build enables CUDA; otherwise it
creates a CPU-only build.

With exactly one NVIDIA GPU, no additional options are required: `main.py`
uses the only GPU automatically and monitors it with the default
`--gpu-index 0`. The GPU must still have enough VRAM for the selected models
and runtime buffers. If it does not, offload fewer layers (`-ngl <number>`) or
use CPU mode with `-ngl 0`.

## 4. Optional manual `llama-bench` setup

Clone and build llama.cpp. Add `-DGGML_CUDA=ON` only if you installed the
CUDA Toolkit in step 2.

### Linux / macOS

```bash
git clone https://github.com/ggml-org/llama.cpp ~/llama.cpp

# CPU-only build:
cmake -S ~/llama.cpp -B ~/llama.cpp/build -DCMAKE_BUILD_TYPE=Release
# ...or, with GPU support:
cmake -S ~/llama.cpp -B ~/llama.cpp/build -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=ON

cmake --build ~/llama.cpp/build --config Release --parallel --target llama-bench
```

The resulting executable is at `~/llama.cpp/build/bin/llama-bench`.

### Windows (PowerShell)

```powershell
git clone https://github.com/ggml-org/llama.cpp $HOME\llama.cpp
cmake -S $HOME\llama.cpp -B $HOME\llama.cpp\build -DCMAKE_BUILD_TYPE=Release
cmake --build $HOME\llama.cpp\build --config Release --target llama-bench
```

Make `llama-bench` discoverable by one of the following (checked in this
order by `main.py`):

1. The `--llama-bench <path>` command-line argument.
2. The `LLAMA_BENCH` environment variable, e.g.
   `export LLAMA_BENCH=~/llama.cpp/build/bin/llama-bench`.
3. A local executable in `Benchmark/`, `Benchmark/bin/`, or the automatically
  built `Benchmark/tools/llama.cpp/` directory.
4. The system `PATH`.
5. An automatic local llama.cpp build.

Verify it works:

```bash
~/llama.cpp/build/bin/llama-bench --help
```

## 5. Set up the Python environment

`main.py` installs its own missing Python dependencies (from
`requirements.txt`) the first time it is run. When the copied folder is used
on its own, run it directly from that folder:

```bash
cd /path/to/Benchmark
python main.py
```

For a separate environment, use the standard library and pip:

```bash
cd /path/to/Benchmark
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 6. Choose the models

Edit [models.json](models.json). Each entry needs the Hugging Face
`repo_id`, the specific `.gguf` `filename`, and a short `label`:

```json
[
    {
        "label": "llama-3.2-3b-q4",
        "repo_id": "bartowski/Llama-3.2-3B-Instruct-GGUF",
        "filename": "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
    }
]
```

The `filename` must be an exact `.gguf` file name from that Hugging Face
repository's file list (**not** an Ollama model tag such as `llama3.2:3b` —
Ollama and Hugging Face use different naming schemes).

Downloaded GGUF files are cached under `Benchmark/models/<label>/`.

For private/gated models or Hugging Face rate limits (HTTP 429), set an access
token before starting the script:

```bash
export HF_TOKEN=your_hugging_face_token
```

## 7. Run the benchmark

```bash
cd /path/to/Benchmark
python main.py
```

Use `--llama-bench` only to override the automatically discovered local build.

### Command-line options

| Argument | Default | Description |
| --- | --- | --- |
| `--llama-bench` | — | Path to the `llama-bench` executable. |
| `-p`, `--prompt` | `512` | Prompt (prefill) size in tokens. |
| `-n`, `--generate` | `128` | Number of tokens to generate (decode). |
| `-ngl`, `--gpu-layers` | `99` | Number of layers to offload to the GPU. |
| `-r`, `--repeats` | `3` | Repetitions per test for averaging. |
| `--gpu-index` | `0` | GPU index to monitor with `nvidia-smi`; it does not select the inference GPU. For multiple GPUs, see `RESULTS.en.md`. |
| `--models-file` | `models.json` | Path to the JSON file listing models. |

Example:

```bash
python main.py --llama-bench ~/llama.cpp/build/bin/llama-bench -p 1024 -n 256
```

## Troubleshooting

- **Missing `git`, `cmake`, or compiler:** install the build tools from step 1.
- **Missing `pip`:** `main.py` tries `ensurepip`; if the OS Python omits it,
  install the distribution's Python `pip` package or use a virtual environment.
- **CPU-only results despite an NVIDIA GPU:** verify `nvcc --version`; remove
  `tools/llama.cpp/build/` and run `python main.py` again to rebuild with CUDA.
- **Insufficient GPU memory:** offload fewer layers with `-ngl <number>` or
  run on the CPU with `-ngl 0`.
- **Download errors:** check internet access; for HTTP 429, set `HF_TOKEN`.
- **Insufficient storage:** delete unneeded cached models from `models/`.

## Output

A comparison table listing, per model, the `pp+tg` test configuration and the
average throughput (tokens/sec) reported by `llama-bench`, plus a second
table with GPU VRAM usage and utilization (if `nvidia-smi` is available).

