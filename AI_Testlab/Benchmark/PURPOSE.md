# Zweck von `main.py`

*[English version see PURPOSE.en.md](PURPOSE.en.md)*

`main.py` ist ein Benchmark-Werkzeug, das die reine Inferenzgeschwindigkeit
(nicht die Genauigkeit) verschiedener lokaler LLMs im GGUF-Format misst und
vergleicht.

## Was das Skript im Detail macht

1. **Abhängigkeiten sicherstellen**: Beim Start prüft `ensure_dependencies()`,
   ob `requests`, `huggingface_hub` und `tqdm` installiert sind. Fehlen sie,
   werden sie automatisch über `pip install -r requirements.txt` nachinstalliert.
2. **Modellliste laden**: `load_models()` liest `models.json` ein. Jede
   Modell-Definition enthält `label` (Kurzname), `repo_id` (Hugging-Face-Repo)
   und `filename` (konkrete `.gguf`-Datei/Quantisierung).
3. **`llama-bench` auflösen**: `resolve_llama_bench()` sucht die
   `llama-bench`-Executable (aus llama.cpp) über `--llama-bench`,
   die Umgebungsvariable `LLAMA_BENCH`, lokale Verzeichnisse oder den `PATH`.
   Falls keine Executable gefunden wird, klont und baut das Skript llama.cpp
   unter `tools/llama.cpp/`; bei vorhandenem `nvcc` wird CUDA aktiviert.
4. **Modelle herunterladen**: `download_model()` lädt für jedes Modell die
   passende GGUF-Datei von Hugging Face herunter (mit Fortschrittsanzeige) und
   cached sie unter `Benchmark/models/<label>/`. Bereits vollständig
   heruntergeladene Dateien werden nicht erneut geladen.
5. **GPU überwachen**: Die Klasse `GpuMonitor` misst währenddessen im
   Hintergrund per `nvidia-smi` den VRAM-Verbrauch und die GPU-Auslastung
   (Baseline vor dem Laden des Modells sowie Peak-Werte während des Benchmarks).
6. **Benchmark ausführen**: `run_llama_bench()` ruft `llama-bench` mit den
   gewählten Parametern (Prompt-/Generierungslänge, GPU-Layer, Wiederholungen)
   für jedes Modell auf und parst die JSON-Ergebnisse.
7. **Ergebnisse zusammenfassen**: `summarize()` gibt eine Vergleichstabelle
   aus mit Tokens/Sekunde je Modell und Testkonfiguration (`prompt+generate`),
   sowie eine zweite Tabelle mit GPU-Kennzahlen (Basis-/Peak-VRAM in GiB,
   effektiver Modell-VRAM-Bedarf, durchschnittliche/maximale GPU-Auslastung).

## Kurz gesagt

Das Skript automatisiert den kompletten Ablauf "Modell herunterladen →
Benchmark mit llama-bench ausführen → Durchsatz und GPU-Ressourcen messen →
Ergebnisse tabellarisch vergleichen", um verschiedene GGUF-Modelle objektiv
hinsichtlich Geschwindigkeit und Ressourcenverbrauch zu vergleichen.
