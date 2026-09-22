#!/usr/bin/env pwsh
# PowerShell version of start-models.sh
# You'll need ollama installed to run this script. You can install it from https://ollama.com/download

$ErrorActionPreference = "Stop"

# Resolve paths so the script works regardless of the current directory.
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

# Pull the Qwen and LLaMA models from Ollama
ollama pull qwen3.5:4b
ollama pull llama3.2:3b

# Create a virtual environment and install the required dependencies
# I use uv for this
Push-Location $RepoRoot
try {
    uv venv

    # Install the Python dependencies into the virtual environment
    uv pip install -r (Join-Path $ScriptDir "requirements.txt")

    # Run the evaluation script (defaults: 10 sampled cases, 3 repeats per model)
    uv run python (Join-Path $ScriptDir "main.py") @args
}
finally {
    Pop-Location
}
