# Benchmark-Ergebnisse interpretieren

*[English version see RESULTS.en.md](RESULTS.en.md)*

Diese Datei erklärt, wie die von `main.py` ausgegebenen Tabellen zu lesen
sind. Siehe [PURPOSE.md](PURPOSE.md) für eine Erklärung, was das Skript tut,
und [README.de.md](README.de.md) für die Installation.

## Beispielausgabe

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

## Tabelle 1: Durchsatz (Tokens/Sekunde)

Jede Spalte steht für eine Testkonfiguration `prompt+generate` (in Tokens):

- **`512+0`** — reine **Prompt-Verarbeitung (Prefill)**: wie schnell das
  Modell einen 512 Token langen Prompt einliest/verarbeitet, bevor es mit der
  Generierung beginnt. Hohe Werte sind hier normal, da Prefill parallelisierbar
  ist (viele Tokens gleichzeitig).
- **`0+64`** — reine **Text-Generierung (Decode)**: wie viele neue Tokens pro
  Sekunde erzeugt werden, ausgehend von einem leeren/kurzen Prompt. Diese Zahl
  ist meist die aussagekräftigste für die "gefühlte" Geschwindigkeit beim
  Chatten, da Decode Token für Token (sequenziell) erfolgt und daher deutlich
  langsamer ist als Prefill.
- **`512+64`** — eine **kombinierte, realistischere Anfrage**: 512 Tokens
  Prompt gefolgt von 64 generierten Tokens. Der Durchsatz liegt erwartungsgemäß
  zwischen den beiden Extremwerten.

**Wie vergleicht man Modelle?**
- Höhere Werte = schneller.
- Für "wie schnell fühlt sich ein Chat an" auf die `0+n`-Spalte (Decode)
  schauen.
- Für "wie schnell werden große Kontexte/Dokumente verarbeitet" auf die
  `p+0`-Spalte (Prefill) schauen.
- Modellgröße und Quantisierung (`Q4_K_M`, `Q6_K`, …) beeinflussen den
  Durchsatz stark: kleinere/stärker quantisierte Modelle sind i. d. R.
  schneller, aber ggf. ungenauer (dieses Tool misst **nicht** die Genauigkeit).

## Tabelle 2: GPU-Kennzahlen

- **`base GiB`** — VRAM-Belegung *bevor* das Modell geladen wurde (Baseline,
  z. B. durch Desktop/andere Prozesse belegt).
- **`peak GiB`** — maximale VRAM-Belegung *während* des gesamten Benchmarks
  (Modell + Laufzeitpuffer wie KV-Cache).
- **`model GiB`** — effektiver VRAM-Bedarf des Modells selbst
  (`peak GiB - base GiB`). Das ist die relevante Zahl, um abzuschätzen, ob ein
  Modell auf die überwachte GPU passt. Bei mehreren sichtbaren GPUs kann
  llama.cpp Modell-Layer verteilen; dann ist dieser Wert nur der Bedarf von
  `--gpu-index`, nicht der Gesamtbedarf über alle GPUs.
- **`avg %` / `peak %`** — durchschnittliche bzw. maximale GPU-Auslastung
  (Rechenleistung, nicht Speicher) während des Benchmarks. Werte nahe 100 %
  zeigen, dass die GPU der limitierende Faktor ist (gut ausgelastet). Niedrige
  Werte (z. B. < 30 %) deuten darauf hin, dass andere Faktoren bremsen — etwa
  CPU-Overhead, fehlendes GPU-Offloading (`-ngl`) oder ein CPU-only-Build von
  `llama-bench` ohne CUDA/Metal/ROCm-Unterstützung.

Falls die GPU-Tabelle den Hinweis `(GPU stats unavailable - nvidia-smi not
found or no samples.)` zeigt, ist entweder keine NVIDIA-GPU vorhanden oder
`nvidia-smi` nicht im `PATH`.

## Typische Fallstricke bei der Interpretation

- **CPU- vs. GPU-Build**: Wurde `llama-bench` ohne `-DGGML_CUDA=ON` (bzw.
  ohne passendes Backend) gebaut, läuft die Inferenz komplett auf der CPU —
  auch wenn eine GPU im System steckt. Das erkennt man an sehr niedriger
  `avg %`/`peak %` (oder `0.0`) trotz vorhandener GPU. Siehe
  [README.md](README.md) für den GPU-Build.
- **`-ngl` (GPU-Layer)**: Ist dieser Wert zu niedrig, werden nur wenige
  Modell-Layer auf die GPU ausgelagert, der Rest läuft auf der CPU — das
  senkt Durchsatz und GPU-Auslastung gleichermaßen.
- **Mehrere GPUs**: `llama-bench` verwendet standardmäßig automatische
  Geräteauswahl und kann Layer verteilen. Das Skript überwacht dagegen nur die
  per `--gpu-index` ausgewählte GPU. Für eindeutig vergleichbare VRAM-Werte
  kann der Prozess auf eine GPU beschränkt werden, z. B.
  `CUDA_VISIBLE_DEVICES=0 python main.py --gpu-index 0`.
- **Eine GPU**: Mit nur einer sichtbaren NVIDIA-GPU sind `-ngl 99` und
  `--gpu-index 0` die passenden Standardwerte. Reicht ihr VRAM nicht aus,
  muss `-ngl` reduziert oder auf `-ngl 0` (CPU) gesetzt werden.
- **Wiederholungen (`-r`)**: Die angezeigten Werte sind bereits über `-r`
  Wiederholungen gemittelt. Eine höhere Wiederholungszahl liefert stabilere,
  aber langsamer ermittelte Ergebnisse.
- **Ergebnisse sind hardwarespezifisch**: Absolute Zahlen lassen sich nur
  zwischen Modellen auf **derselben** Maschine sinnvoll vergleichen, nicht
  zwischen unterschiedlicher Hardware.
