# Ollama mit NVIDIA-GPU und Open WebUI mit Docker Compose

Diese Umgebung stellt **Ollama** und **Open WebUI** in zwei getrennten Docker-Containern bereit.
Ollama erhält Zugriff auf die NVIDIA-GPU. Open WebUI kommuniziert über ein internes Docker-Netzwerk mit Ollama und ist über TCP-Port **3000** erreichbar.

## Architektur

```text
Browser
   |
   | http://<XUBUNTU-IP>:3000
   v
+---------------------+
| Open WebUI           |
| Port 8080 im Container
+----------+----------+
           |
           | Docker-Netzwerk ai_backend
           | http://ollama:11434
           v
+---------------------+
| Ollama               |
| NVIDIA GPU           |
| Port 11434 intern    |
+---------------------+
```

Der Ollama-Port `11434` wird in dieser Konfiguration absichtlich **nicht auf dem Xubuntu-Host veröffentlicht**. Dadurch ist die Ollama-API nur für Container im Docker-Netzwerk erreichbar.

---

## 1. Voraussetzungen

Empfohlen wird ein aktuelles Xubuntu auf Basis einer unterstützten Ubuntu-Version, beispielsweise Ubuntu/Xubuntu 24.04 oder neuer.

Erforderlich sind:

- NVIDIA-Grafikkarte, die von Ollama unterstützt wird
- aktueller NVIDIA-Treiber auf dem Xubuntu-Host
- Docker Engine
- Docker Compose v2 (`docker compose`)
- NVIDIA Container Toolkit
- ausreichend Arbeitsspeicher, VRAM und freier Festplattenspeicher für die gewünschten Modelle

Ollama unterstützt unter Linux NVIDIA-GPUs mit geeigneter Compute Capability; die aktuelle Ollama-Dokumentation nennt Compute Capability 5.0+ und einen NVIDIA-Treiber ab Version 531.

### NVIDIA-Treiber prüfen

```bash
nvidia-smi
```

Die NVIDIA-GPU und die installierte Treiberversion sollten angezeigt werden.

### Docker prüfen

```bash
docker --version
docker compose version
```

Falls Docker noch nicht installiert ist, kann es wie im folgenden Abschnitt beschrieben eingerichtet werden.

### Docker Engine installieren

Benötigte Pakete installieren und das offizielle Docker-Repository einrichten:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
```

Docker Engine, die CLI, containerd sowie die Plugins Buildx und Compose installieren:

```bash
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Installation testen:

```bash
sudo docker run hello-world
```

Optional: Den aktuellen Benutzer der Gruppe `docker` hinzufügen, damit Docker-Befehle ohne `sudo` ausgeführt werden können. Danach ist eine Ab- und erneute Anmeldung erforderlich:

```bash
sudo usermod -aG docker $USER
```

Anschliessend die Installation erneut prüfen:

```bash
docker --version
docker compose version
```

---

## 2. NVIDIA Container Toolkit installieren

Benötigte Pakete installieren:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
```

NVIDIA Repository einrichten:

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

Paketlisten aktualisieren und Toolkit installieren:

```bash
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```

Docker für den NVIDIA Container Runtime konfigurieren:

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

GPU-Zugriff aus Docker testen:

```bash
docker run --rm --gpus all ubuntu nvidia-smi
```

Wenn auch innerhalb des Testcontainers die NVIDIA-GPU angezeigt wird, ist die GPU-Passthrough-Konfiguration funktionsfähig.

---

## 3. Projektverzeichnis vorbereiten

Beispiel:

```bash
mkdir -p ~/ollama-openwebui
cd ~/ollama-openwebui
```

Die Datei `docker-compose.yml` in dieses Verzeichnis kopieren.

Die Verzeichnisstruktur sieht anschliessend beispielsweise so aus:

```text
~/ollama-openwebui/
├── docker-compose.yml
└── README.md
```

---

## 4. Open-WebUI Secret Key erstellen

Open WebUI sollte mit einem dauerhaft gesetzten `WEBUI_SECRET_KEY` betrieben werden. Der Schlüssel wird unter anderem für die Signierung von Sitzungen verwendet und sollte sich bei einem Neustart oder beim Neuerstellen des Containers nicht ändern.

Zuerst einen zufälligen Schlüssel mit OpenSSL erzeugen:

```bash
openssl rand -hex 32
```

Die Ausgabe sieht beispielsweise so aus:

```text
8d2c71a2f4c95f0d8c1b6e4f0b6c2e0a9f7a13d4b8c6e1f275f6348af8df90bc
```

Im Projektverzeichnis eine Datei `.env` erstellen:

```bash
nano .env
```

Den erzeugten Schlüssel dort eintragen:

```text
WEBUI_SECRET_KEY=HIER_DEN_GENERIERTEN_SCHLUESSEL_EINTRAGEN
```

Alternativ kann die `.env`-Datei direkt in einem Schritt erzeugt werden:

```bash
printf 'WEBUI_SECRET_KEY=%s\n' "$(openssl rand -hex 32)" > .env
chmod 600 .env
```

Die Verzeichnisstruktur sieht danach beispielsweise so aus:

```text
~/ollama-openwebui/
├── .env
├── docker-compose.yml
└── README.md
```

> Die Datei `.env` enthält ein Geheimnis und sollte nicht in ein öffentliches Git-Repository eingecheckt oder weitergegeben werden.

Die Compose-Datei übernimmt den Schlüssel mit:

```yaml
environment:
  WEBUI_SECRET_KEY: ${WEBUI_SECRET_KEY}
```

---

## 5. Container Images herunterladen

```bash
docker compose pull
```

Verwendet werden:

- `ollama/ollama:latest`
- `ghcr.io/open-webui/open-webui:v0.11.1`

Für produktive Umgebungen empfiehlt es sich, nach erfolgreichem Test feste Image-Versionen statt beweglicher Tags wie `latest` oder `main` zu verwenden.

---

## 6. Umgebung starten

```bash
docker compose up -d
```

Status prüfen:

```bash
docker compose ps
```

Die beiden Container sollten als gestartet angezeigt werden:

```text
ollama
open-webui
```

Logs anzeigen:

```bash
docker compose logs -f
```

Nur Ollama:

```bash
docker compose logs -f ollama
```

Nur Open WebUI:

```bash
docker compose logs -f open-webui
```

---

## 7. Erstes Ollama-Modell installieren

Ein Modell wird direkt im Ollama-Container heruntergeladen. Beispiel mit `llama3.2`:

```bash
docker compose exec ollama ollama pull llama3.2
```

Installierte Modelle anzeigen:

```bash
docker compose exec ollama ollama list
```

Modell testweise in der Konsole starten:

```bash
docker compose exec ollama ollama run llama3.2
```

Die interaktive Ollama-Sitzung kann mit `Ctrl+D` beendet werden.

---

## 8. Browser-Zugriff auf Open WebUI

### Zugriff direkt auf dem Xubuntu-System

```text
http://localhost:3000
```

### Zugriff von einem anderen Computer im Netzwerk

IP-Adresse des Xubuntu-Systems anzeigen:

```bash
hostname -I
```

Anschliessend im Browser beispielsweise:

```text
http://192.168.1.50:3000
```

Dabei `192.168.1.50` durch die tatsächliche IP-Adresse des Xubuntu-Systems ersetzen.

Beim ersten Aufruf von Open WebUI wird normalerweise das erste Benutzerkonto angelegt. Dieses erste Konto besitzt administrative Rechte.

Falls auf Xubuntu eine Firewall aktiv ist, muss TCP-Port `3000` für die gewünschten Quellnetze freigegeben werden. Beispiel für ein lokales Netz mit UFW:

```bash
sudo ufw allow from 192.168.1.0/24 to any port 3000 proto tcp
```

Die Netzadresse muss an die eigene Umgebung angepasst werden.

> Für einen produktiven oder über das Internet erreichbaren Betrieb sollte Open WebUI nicht unverschlüsselt direkt auf Port 3000 veröffentlicht werden. Verwenden Sie einen Reverse Proxy mit HTTPS und geeigneten Zugriffsregeln.

---

## 9. Verbindung Open WebUI zu Ollama

Die Verbindung wird in `docker-compose.yml` automatisch konfiguriert:

```yaml
environment:
  OLLAMA_BASE_URL: http://ollama:11434
  ENABLE_OLLAMA_API: "True"
```

`ollama` ist dabei der Docker-Service-Name. Docker stellt innerhalb des gemeinsamen Netzwerks `ai_backend` automatisch die Namensauflösung bereit.

Der Ollama-Port wird nur intern mit `expose` bekannt gemacht und nicht mit `ports` auf dem Host veröffentlicht.

---

## 10. GPU-Nutzung überprüfen

Zuerst in Open WebUI eine Anfrage an ein Ollama-Modell senden oder das Modell über die CLI starten.

Danach auf dem Xubuntu-Host:

```bash
nvidia-smi
```

Zusätzlich kann Ollama anzeigen, ob ein geladenes Modell auf CPU oder GPU ausgeführt wird:

```bash
docker compose exec ollama ollama ps
```

In der Spalte `PROCESSOR` bedeutet beispielsweise `100% GPU`, dass das Modell vollständig in den Grafikspeicher geladen wurde. Bei zu wenig VRAM kann Ollama ein Modell teilweise auf CPU und GPU verteilen.

---

## 11. Container stoppen und starten

Stoppen:

```bash
docker compose stop
```

Wieder starten:

```bash
docker compose start
```

Container entfernen, persistente Daten aber behalten:

```bash
docker compose down
```

Die Modelle und Open-WebUI-Daten bleiben in Docker Volumes erhalten.

---

## 12. Aktualisieren

Neue Container Images herunterladen:

```bash
docker compose pull
```

Container mit den neuen Images neu erstellen:

```bash
docker compose up -d
```

Nicht mehr benötigte Images können anschliessend optional entfernt werden:

```bash
docker image prune
```

Bei produktiven Installationen sollten neue Versionen zunächst getestet und Image-Tags bewusst versioniert werden.

---

## 13. Persistente Daten

Die Compose-Datei verwendet zwei benannte Docker Volumes:

```text
ollama_data       -> Ollama-Modelle und Ollama-Daten
open_webui_data   -> Benutzer, Einstellungen, Chats und Open-WebUI-Daten
```

Volumes anzeigen:

```bash
docker volume ls
```

> Achtung: `docker compose down -v` löscht auch die persistenten Volumes und damit unter anderem heruntergeladene Ollama-Modelle und Open-WebUI-Daten.

---

## 14. Nützliche Befehle

```bash
# Status
docker compose ps

# Alle Logs
docker compose logs -f

# Modelle anzeigen
docker compose exec ollama ollama list

# Modell herunterladen
docker compose exec ollama ollama pull llama3.2

# Geladene Modelle und CPU/GPU-Nutzung anzeigen
docker compose exec ollama ollama ps

# Ollama neu starten
docker compose restart ollama

# Open WebUI neu starten
docker compose restart open-webui

# Gesamte Umgebung neu starten
docker compose restart
```

---

## 15. Fehleranalyse

### Docker erkennt die NVIDIA-GPU nicht

Folgenden Test ausführen:

```bash
docker run --rm --gpus all ubuntu nvidia-smi
```

Wenn dieser Befehl fehlschlägt, zuerst NVIDIA-Treiber und NVIDIA Container Toolkit prüfen.

### Ollama verwendet nur die CPU

Prüfen:

```bash
nvidia-smi
docker compose logs ollama
docker compose exec ollama ollama ps
```

Ollama empfiehlt bei GPU-Erkennungsproblemen ausserdem, die NVIDIA-Treiber aktuell zu halten und zunächst sicherzustellen, dass der Docker-GPU-Test mit `nvidia-smi` funktioniert.

### Open WebUI zeigt keine Ollama-Modelle

Prüfen, ob das Modell installiert ist:

```bash
docker compose exec ollama ollama list
```

Prüfen, ob beide Container laufen:

```bash
docker compose ps
```

Ollama- und Open-WebUI-Logs prüfen:

```bash
docker compose logs ollama
docker compose logs open-webui
```

Die konfigurierte Ollama-Adresse muss innerhalb des Docker-Netzwerks `http://ollama:11434` lauten.

---

## Offizielle Dokumentation

- Ollama Docker: https://docs.ollama.com/docker
- Ollama GPU-Unterstützung: https://docs.ollama.com/gpu
- Ollama FAQ: https://docs.ollama.com/faq
- Open WebUI Quick Start: https://docs.openwebui.com/getting-started/quick-start/
- Open WebUI Environment Variables: https://docs.openwebui.com/reference/env-configuration/
- NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
- Docker Compose GPU Support: https://docs.docker.com/compose/how-tos/gpu-support/

