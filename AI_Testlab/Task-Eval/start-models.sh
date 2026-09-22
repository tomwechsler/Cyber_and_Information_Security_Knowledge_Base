#!/usr/bin/env bash
set -euo pipefail

# Resolve paths so the script works regardless of the current directory.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# You'll need ollama installed to run this script. You can install it from https://ollama.com/download

# Pull the Qwen and LLaMA models from Ollama
ollama pull qwen3.5:4b
ollama pull llama3.2:3b

# Create a virtual environment and install the required dependencies
# I use uv for this
cd "$REPO_ROOT"
uv venv

# Install the Python dependencies into the virtual environment
uv pip install -r "$SCRIPT_DIR/requirements.txt"

# Run the evaluation script (defaults: 10 sampled cases, 3 repeats per model)
uv run python "$SCRIPT_DIR/main.py" "$@"
