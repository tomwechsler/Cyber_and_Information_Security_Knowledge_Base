# Benchmark

*[English version see README.md](README.md)*

Lädt GGUF-Modelldateien vom Hugging Face Hub herunter und misst deren reine
Inferenzgeschwindigkeit mit `llama-bench` (aus llama.cpp).

Im Gegensatz zu `Task-Eval` prüft dieses Werkzeug **nicht** die Genauigkeit —
es misst Prompt-Verarbeitung (Prefill) und Text-Generierung (Decode) in
Tokens/Sekunde.

Eine detaillierte Erklärung, was `main.py` intern tut, findet sich in
[PURPOSE.md](PURPOSE.md).

## Voraussetzungen

- **Python 3.10+**
- **cmake**, ein C/C++-Compiler (`gcc`/`g++`) und `git` — nötig, um
  llama.cpp beim ersten Start aus dem Quellcode zu bauen.
- **Internetzugang** — beim ersten Start nötig, um llama.cpp zu klonen und
  Modelle von Hugging Face herunterzuladen.
- **Freier Speicherplatz** — für die enthaltenen Modelle und den lokalen
  llama.cpp-Build etwa 15 GiB einplanen; der genaue Bedarf hängt von
  `models.json` ab.
- (Optional) **NVIDIA-GPU + CUDA-Toolkit** — um mit GPU-Offloading statt
  reiner CPU-Inferenz zu benchmarken.

## 1. Build-Werkzeuge installieren

### Linux (Debian/Ubuntu)

```bash
sudo apt-get update
sudo apt-get install -y cmake gcc g++ git
```

### Windows

[CMake](https://cmake.org/download/), [Git](https://git-scm.com/) und eine
C++-Toolchain installieren (z. B. Visual Studio Build Tools mit der
Workload "Desktopentwicklung mit C++").

## 2. (Optional) CUDA-Toolkit für GPU-Unterstützung installieren

Diesen Schritt überspringen, wenn nur auf der CPU benchmarkt werden soll.

### Linux (Debian/Ubuntu)

```bash
sudo apt-get install -y nvidia-cuda-toolkit
```

Prüfen mit:

```bash
nvcc --version
nvidia-smi
```

### Windows

Das [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
installieren.

## 3. Automatische Einrichtung von `llama-bench`

Falls keine Executable angegeben ist, klont und baut `main.py` beim ersten
Start `llama.cpp` inklusive `llama-bench` automatisch unter
`Benchmark/tools/llama.cpp/`. Der Ordner `Benchmark` kann damit auf ein neues
System kopiert und ohne Installation von llama.cpp oder Anpassung des `PATH`
ausgeführt werden. `git`, `cmake` und ein C++-Compiler werden weiterhin
benötigt. Die gebaute Executable wird bei späteren Starts wiederverwendet.
Wenn `nvcc` vorhanden ist, aktiviert der automatische Build CUDA; andernfalls
wird ein CPU-Build erstellt.

Mit genau einer NVIDIA-GPU sind keine weiteren Optionen nötig: `main.py`
verwendet die einzige GPU automatisch und überwacht sie mit dem Standardwert
`--gpu-index 0`. Der VRAM der GPU muss jedoch für die gewählten Modelle und
die Laufzeitpuffer ausreichen. Bei Speichermangel weniger Layer auslagern
(`-ngl <zahl>`) oder CPU-Betrieb mit `-ngl 0` verwenden.

## 4. Optionale manuelle Einrichtung von `llama-bench`

llama.cpp klonen und bauen. `-DGGML_CUDA=ON` nur hinzufügen, wenn in Schritt 2
das CUDA-Toolkit installiert wurde.

### Linux / macOS

```bash
git clone https://github.com/ggml-org/llama.cpp ~/llama.cpp

# Reiner CPU-Build:
cmake -S ~/llama.cpp -B ~/llama.cpp/build -DCMAKE_BUILD_TYPE=Release
# ...oder mit GPU-Unterstützung:
cmake -S ~/llama.cpp -B ~/llama.cpp/build -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=ON

cmake --build ~/llama.cpp/build --config Release --parallel --target llama-bench
```

Die fertige Executable liegt unter `~/llama.cpp/build/bin/llama-bench`.

### Windows (PowerShell)

```powershell
git clone https://github.com/ggml-org/llama.cpp $HOME\llama.cpp
cmake -S $HOME\llama.cpp -B $HOME\llama.cpp\build -DCMAKE_BUILD_TYPE=Release
cmake --build $HOME\llama.cpp\build --config Release --target llama-bench
```

`llama-bench` auf eine der folgenden Arten auffindbar machen (wird von
`main.py` in dieser Reihenfolge geprüft):

1. Das Kommandozeilenargument `--llama-bench <pfad>`.
2. Die Umgebungsvariable `LLAMA_BENCH`, z. B.
   `export LLAMA_BENCH=~/llama.cpp/build/bin/llama-bench`.
3. Eine lokale Executable in `Benchmark/`, `Benchmark/bin/` oder im
  automatisch gebauten Verzeichnis `Benchmark/tools/llama.cpp/`.
4. Der System-`PATH`.
5. Ein automatischer lokaler llama.cpp-Build.

Funktionstest:

```bash
~/llama.cpp/build/bin/llama-bench --help
```

## 5. Python-Umgebung einrichten

`main.py` installiert beim ersten Start fehlende Python-Abhängigkeiten (aus
`requirements.txt`) automatisch selbst. Wird der kopierte Ordner eigenständig
verwendet, wird das Skript direkt daraus gestartet:

```bash
cd /pfad/zu/Benchmark
python main.py
```

Für eine separate Umgebung genügen Standardbibliothek und pip:

```bash
cd /pfad/zu/Benchmark
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 6. Modelle auswählen

[models.json](models.json) bearbeiten. Jeder Eintrag braucht das
Hugging-Face-`repo_id`, den konkreten `.gguf`-`filename` und ein kurzes
`label`:

```json
[
    {
        "label": "llama-3.2-3b-q4",
        "repo_id": "bartowski/Llama-3.2-3B-Instruct-GGUF",
        "filename": "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
    }
]
```

Der `filename` muss ein exakter `.gguf`-Dateiname aus der Dateiliste des
jeweiligen Hugging-Face-Repos sein (**kein** Ollama-Modell-Tag wie
`llama3.2:3b` — Ollama und Hugging Face verwenden unterschiedliche
Namensschemata).

Heruntergeladene GGUF-Dateien werden unter `Benchmark/models/<label>/`
gecacht.

Bei privaten/geschützten Modellen oder Hugging-Face-Rate-Limits (HTTP 429)
vor dem Start einen Zugriffstoken setzen:

```bash
export HF_TOKEN=ihr_hugging_face_token
```

## 7. Benchmark ausführen

```bash
cd /pfad/zu/Benchmark
python main.py
```

`--llama-bench` wird nur benötigt, um die automatisch erkannte lokale
Executable zu überschreiben.

### Kommandozeilenoptionen

| Argument | Standard | Beschreibung |
| --- | --- | --- |
| `--llama-bench` | — | Pfad zur `llama-bench`-Executable. |
| `-p`, `--prompt` | `512` | Prompt-Größe (Prefill) in Tokens. |
| `-n`, `--generate` | `128` | Anzahl zu generierender Tokens (Decode). |
| `-ngl`, `--gpu-layers` | `99` | Anzahl der auf die GPU ausgelagerten Layer. |
| `-r`, `--repeats` | `3` | Wiederholungen pro Test zur Mittelwertbildung. |
| `--gpu-index` | `0` | GPU-Index für `nvidia-smi`; wählt nicht die Inferenz-GPU aus. Bei mehreren GPUs siehe `RESULTS.md`. |
| `--models-file` | `models.json` | Pfad zur JSON-Datei mit der Modellliste. |

Beispiel:

```bash
python main.py --llama-bench ~/llama.cpp/build/bin/llama-bench -p 1024 -n 256
```

## Fehlerbehebung

- **`git`, `cmake` oder Compiler fehlen:** Build-Werkzeuge aus Schritt 1
  installieren.
- **`pip` fehlt:** `main.py` versucht `ensurepip`; falls dieses im
  Betriebssystem-Python fehlt, das Python-`pip`-Paket installieren oder eine
  virtuelle Umgebung verwenden.
- **Trotz NVIDIA-GPU nur CPU-Ergebnisse:** `nvcc --version` prüfen,
  `tools/llama.cpp/build/` löschen und `python main.py` erneut starten.
- **Zu wenig GPU-Speicher:** weniger Layer mit `-ngl <zahl>` auslagern oder
  mit `-ngl 0` auf der CPU ausführen.
- **Downloadfehler:** Internetzugang prüfen; bei HTTP 429 `HF_TOKEN` setzen.
- **Zu wenig Speicher:** nicht benötigte Modell-Caches unter `models/` löschen.

## Ausgabe

Eine Vergleichstabelle mit der `pp+tg`-Testkonfiguration und dem
durchschnittlichen Durchsatz (Tokens/Sekunde) je Modell laut `llama-bench`,
sowie eine zweite Tabelle mit GPU-VRAM-Verbrauch und -Auslastung (falls
`nvidia-smi` verfügbar ist).
