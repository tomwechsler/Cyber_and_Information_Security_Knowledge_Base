# Task-Eval

*[English version see README.md](README.md)*

Ein kleines Evaluierungswerkzeug, das Support-Tickets mit lokalen
Ollama-Modellen klassifiziert, deren Genauigkeit vergleicht und
Performance-, Speicher- und GPU-Nutzung ausgibt.

Das Skript ([main.py](main.py)) lässt jedes Modell gegen zufällige
Stichproben aus [eval-cases.json](eval-cases.json) laufen und gibt eine
Vergleichsübersicht aus.

Eine detaillierte Erklärung, was `main.py` intern tut, findet sich in
[PURPOSE.md](PURPOSE.md), und wie die ausgegebenen Tabellen zu interpretieren
sind, in [RESULTS.md](RESULTS.md).

## Voraussetzungen

- **Ollama** — führt die lokalen Modelle aus.
- **Python 3.10+**

`main.py` ist vollständig eigenständig und portabel: Bei jedem Start erstellt
es bei Bedarf sein eigenes virtuelles Environment (`.venv` in diesem
Verzeichnis) — auf Systemen ohne `ensurepip` wird `pip` automatisch
nachgeladen —, installiert fehlende Python-Abhängigkeiten (aus
`requirements.txt`), startet sich selbst in diesem Environment neu, prüft,
ob der Ollama-Server erreichbar ist, und lädt alle benötigten Modelle
(`llama3.2:3b`, `qwen3.5:4b`) automatisch nach, falls sie lokal noch nicht
vorhanden sind. Das Verzeichnis kann auf jedes System mit Python 3.10+
kopiert werden — die einzige manuelle Voraussetzung ist die Installation und
der Start von Ollama selbst.

- **NVIDIA-GPU (optional)** — die GPU-Nutzungstabelle (Auslastung,
  Leistungsaufnahme, Speicher) wird über `nvidia-smi` erfasst und benötigt
  daher eine NVIDIA-Karte mit installierten Treibern. Auf Systemen ohne
  `nvidia-smi` läuft das Skript trotzdem; der GPU-Abschnitt zeigt dann
  lediglich "nvidia-smi unavailable / no samples" an.

## 1. Ollama installieren

Von https://ollama.com/download herunterladen und installieren, danach
prüfen, ob es läuft:

```bash
ollama --version
```

Die Ollama-App/den Dienst starten, damit dessen API unter
`http://localhost:11434` erreichbar ist. `main.py` bricht mit einer klaren
Fehlermeldung ab, falls diese URL nicht erreichbar ist.

## 2. Python-Umgebung einrichten (nicht erforderlich)

`main.py` verwaltet seine Python-Umgebung selbst: Beim ersten Start erstellt
es `.venv` in diesem Verzeichnis, installiert die Abhängigkeiten aus
`requirements.txt` dort hinein und startet sich selbst mit dieser Umgebung
neu. Das funktioniert auch, wenn `ensurepip`/`python3-venv` nicht verfügbar
ist (häufig unter Debian/Ubuntu) — pip wird dann über `get-pip.py`
nachgeladen — und unabhängig davon, ob gerade ein anderes virtuelles
Environment aktiv ist. Ein manueller `venv`-/`pip`-Schritt ist nicht nötig;
beim ersten Lauf wird eine Internetverbindung zum Herunterladen der Pakete
benötigt.

Wer die Umgebung dennoch vorab einrichten möchte:

```bash
cd Task-Eval
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt   # Windows: .venv\Scripts\pip install -r requirements.txt
```

## 3. Evaluierung ausführen

```bash
cd Task-Eval
python3 main.py
```

Unter Windows stattdessen `py main.py` verwenden. Wenn nur dieses
Verzeichnis kopiert wurde, zuerst in dieses Verzeichnis wechseln und dort
denselben Befehl ausführen.

Beim ersten Lauf werden fehlende Modelle automatisch geladen
(`ollama pull llama3.2:3b`, `ollama pull qwen3.5:4b`) — ein manueller
`ollama pull`-Schritt ist nicht nötig. Standardmäßig werden 10 Fälle pro
Durchlauf gezogen, 3 Wiederholungen pro Modell durchgeführt und ein
Fortschrittsbalken gefolgt von einer Vergleichsübersicht angezeigt.

### Kommandozeilenoptionen

| Argument | Standard | Beschreibung |
| --- | --- | --- |
| `-n`, `--sample-size` | `10` | Anzahl zufällig gezogener Fälle pro Durchlauf. |
| `-x`, `--repeats` | `3` | Anzahl Durchläufe, jeweils mit neuer Zufallsstichprobe. |
| `--show-cases` | aus | Jeden Fall einzeln ausgeben statt Fortschrittsbalken. |
| `-h`, `--help` | — | Hilfe anzeigen und beenden. |

Beispiele:

```bash
# Größere Evaluierung: 20 Fälle, 5 Durchläufe
python3 Task-Eval/main.py -n 20 -x 5

# Jeden Fall bei der Verarbeitung anzeigen
python3 Task-Eval/main.py --show-cases
```

### Optional: `start-models.sh` / `start-models.ps1`

[start-models.sh](start-models.sh) und [start-models.ps1](start-models.ps1)
sind Komfort-Wrapper, die die `uv`-Umgebung einrichten und `main.py` in einem
Schritt ausführen. Sie sind nicht mehr zwingend erforderlich (da `main.py`
Abhängigkeiten und Modelle nun selbst einrichtet), bleiben aber für alle
erhalten, die ein All-in-one-Skript bevorzugen.

## Ausgabe

Das Skript gibt zwei Tabellen aus:

- **Modell-Vergleichsübersicht** — Genauigkeit bei Kategorie/Dringlichkeit/
  exakter Übereinstimmung, Durchsatz (Tokens/Sekunde), durchschnittliche
  Latenz sowie Speicher-/VRAM-Bedarf des Modells (über Ollamas
  `/api/ps`-Endpunkt).
- **GPU-Nutzung** — durchschnittliche und maximale GPU-Auslastung,
  Leistungsaufnahme und maximaler GPU-Speicher, gemessen mit `nvidia-smi`
  während des Laufs jedes Modells. **Benötigt eine NVIDIA-GPU.**

Jedes Modell wird bei Bedarf geladen und nach seinem Lauf wieder entladen,
damit die Statistiken pro Modell isoliert sind.
