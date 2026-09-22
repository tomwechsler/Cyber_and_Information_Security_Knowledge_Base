# Zweck von `main.py`

*[English version see PURPOSE.en.md](PURPOSE.en.md)*

`main.py` ist ein Evaluierungswerkzeug, das die **Klassifikationsgenauigkeit**
(nicht die reine Geschwindigkeit) verschiedener lokaler Ollama-Modelle bei
einer konkreten Aufgabe misst und vergleicht: der Klassifikation von
Support-Tickets.

## Was das Skript im Detail macht

1. **Abhängigkeiten sicherstellen**: Beim Start prüft `ensure_dependencies()`,
   ob `requests` und `tqdm` installiert sind. Fehlen sie, werden sie
   automatisch über `pip install -r requirements.txt` nachinstalliert.
2. **Ollama-Server prüfen**: `ensure_ollama_running()` prüft, ob die
   Ollama-API unter `http://localhost:11434` erreichbar ist. Falls nicht,
   bricht das Skript mit einer klaren Fehlermeldung ab.
3. **Modelle sicherstellen**: `ensure_models_pulled()` fragt die Liste lokal
   vorhandener Modelle ab (`/api/tags`) und lädt fehlende Modelle aus
   `MODELS` (`llama3.2:3b`, `qwen3.5:4b`) automatisch per
   `ollama pull <modell>` nach.
4. **Testfälle laden**: Beim Import wird [eval-cases.json](eval-cases.json)
   eingelesen — eine Liste von Support-Tickets mit erwarteter `category` und
   `urgency`.
5. **Modell laden & Speicher messen**: Für jedes Modell wird es zunächst per
   `load_model()` in den Ollama-Arbeitsspeicher geladen, damit die spätere
   Zeitmessung nicht durch den Ladevorgang verfälscht wird.
6. **GPU überwachen**: Die Klasse `GpuMonitor` misst währenddessen im
   Hintergrund per `nvidia-smi` GPU-Auslastung, Speicherverbrauch und
   Leistungsaufnahme.
7. **Evaluieren**: `evaluate()` zieht pro Wiederholung (`-x`/`--repeats`)
   eine zufällige Stichprobe (`-n`/`--sample-size`) aus den Testfällen, ruft
   für jedes Ticket `call_ollama()` auf (das Modell muss strukturiertes JSON
   gemäß `SCHEMA` mit `category`, `urgency` und `reason` zurückgeben) und
   vergleicht das Ergebnis mit der erwarteten Kategorie/Dringlichkeit.
8. **Kennzahlen sammeln**: Aus den Ollama-Antworten werden Trefferquote
   (Kategorie, Dringlichkeit, exakte Übereinstimmung), Tokens/Sekunde,
   durchschnittliche Latenz sowie Speicher-/VRAM-Bedarf (`/api/ps`) berechnet.
9. **Modell entladen**: Nach der Auswertung wird das Modell per
   `unload_model()` wieder aus dem Speicher entfernt, damit die Messungen
   der Modelle sich nicht gegenseitig beeinflussen.
10. **Ergebnisse zusammenfassen**: `print_summary()` gibt zwei Tabellen aus:
    eine Vergleichsübersicht (Genauigkeit, Durchsatz, Latenz, Speicher) und
    eine GPU-Nutzungstabelle (Auslastung, Leistungsaufnahme, Spitzenspeicher).

## Kurz gesagt

Das Skript automatisiert den kompletten Ablauf "Modell laden → auf
zufälligen Ticket-Stichproben klassifizieren lassen → Genauigkeit und
Performance messen → Modell entladen → Ergebnisse tabellarisch vergleichen",
um verschiedene Ollama-Modelle objektiv hinsichtlich Klassifikationsgüte,
Geschwindigkeit und Ressourcenverbrauch bei derselben Aufgabe zu vergleichen.
