# Evaluierungs-Ergebnisse interpretieren

*[English version see RESULTS.en.md](RESULTS.en.md)*

Diese Datei erklärt, wie die von `main.py` ausgegebenen Tabellen zu lesen
sind. Siehe [PURPOSE.md](PURPOSE.md) für eine Erklärung, was das Skript tut,
und [README.md](README.md) für die Installation.

## Beispielausgabe

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

## Tabelle 1: Modell-Vergleichsübersicht

- **`Category`** — Anteil der Fälle, bei denen die vom Modell zurückgegebene
  Ticket-**Kategorie** (`billing`, `technical`, `account`, `security`,
  `feature_request`) mit der erwarteten Kategorie übereinstimmt.
- **`Urgency`** — Anteil der Fälle, bei denen die zurückgegebene
  **Dringlichkeit** (`low`, `medium`, `high`) korrekt ist.
- **`Exact`** — Anteil der Fälle, bei denen **sowohl** Kategorie **als auch**
  Dringlichkeit korrekt sind (strengster Genauigkeitswert).
- **`Tok/s`** — Durchsatz bei der Text-Generierung (Tokens/Sekunde), aus
  Ollamas `eval_count`/`eval_duration` berechnet. Höher = schneller.
- **`Latency(s)`** — durchschnittliche Antwortzeit pro Anfrage (Ende-zu-Ende,
  inkl. Prompt-Verarbeitung), in Sekunden. Niedriger = schneller.
- **`Memory(MB)`** — Gesamtgröße des geladenen Modells laut Ollama
  (`/api/ps`, Feld `size`).
- **`VRAM(MB)` `(x%)`** — Anteil des Modells, der tatsächlich im GPU-Speicher
  liegt (Feld `size_vram`), sowie der Prozentsatz `VRAM / Memory`. Ein Wert
  nahe 100 % bedeutet, dass das Modell vollständig auf der GPU läuft; ein
  niedrigerer Wert deutet auf teilweises CPU-Offloading hin (z. B. weil das
  Modell nicht komplett in den VRAM passt).

**Wie vergleicht man Modelle?**
- Für **Aufgabenqualität**: `Category`, `Urgency` und vor allem `Exact`
  vergleichen — höher ist besser.
- Für **Geschwindigkeit**: `Tok/s` (höher besser) und `Latency(s)` (niedriger
  besser) vergleichen.
- Es gibt oft einen Zielkonflikt: größere Modelle (mehr `Memory(MB)`) sind
  häufig genauer, aber langsamer (niedrigeres `Tok/s`, höhere `Latency(s)`).
- Die Anzahl der Stichproben (`-n`) und Wiederholungen (`-x`) beeinflusst,
  wie stabil/aussagekräftig die Prozentwerte sind — bei kleinen `-n`-Werten
  können einzelne Fehlklassifikationen die Prozentzahl stark verschieben.

## Tabelle 2: GPU-Nutzung

- **`Avg Util%` / `Peak Util%`** — durchschnittliche bzw. maximale
  GPU-Auslastung (Rechenleistung) während des Modell-Laufs. Werte nahe
  100 % zeigen, dass die GPU der limitierende Faktor ist.
- **`Avg Power(W)` / `Peak Power(W)`** — durchschnittliche bzw. maximale
  Leistungsaufnahme der GPU in Watt während des Laufs — ein grober Indikator
  für Energieverbrauch/Effizienz.
- **`Peak Mem(MB)`** — maximaler GPU-Speicherverbrauch (gesamtes System,
  nicht nur dieses Modell) während des Laufs.

Wenn diese Tabelle `nvidia-smi unavailable / no samples` anzeigt, ist keine
NVIDIA-GPU vorhanden oder `nvidia-smi` nicht im `PATH`.

## Typische Fallstricke bei der Interpretation

- **Kleine Stichproben täuschen**: Mit `-n 10` kann ein einziger falsch
  klassifizierter Fall die Genauigkeit bereits um 10 Prozentpunkte
  verschieben. Für belastbarere Zahlen `-n` und/oder `-x` erhöhen.
  Da beide Skripte identisches Testmaterial für alle Modelle verwenden,
  bleiben Vergleiche zwischen Modellen dennoch fair.
- **Ergebnisse sind hardware- und modellversionsspezifisch**: Absolute
  Zahlen (besonders `Tok/s`, `Latency`, GPU-Werte) lassen sich nur zwischen
  Modellen auf **derselben** Maschine sinnvoll vergleichen.
- **`temperature: 0`**: Das Skript ruft Ollama mit `temperature=0` auf
  (deterministisch), daher sollten wiederholte Läufe mit denselben Tickets
  zu denselben Klassifikationsergebnissen führen — Schwankungen zwischen
  Wiederholungen (`-x`) entstehen primär durch die zufällige Auswahl
  unterschiedlicher Ticket-Stichproben, nicht durch Modell-Zufälligkeit.
- **VRAM-Prozentsatz < 100 %**: Kann bedeuten, dass das Modell teilweise auf
  der CPU läuft (langsamer) — meist relevant bei großen Modellen auf GPUs
  mit wenig Speicher.
