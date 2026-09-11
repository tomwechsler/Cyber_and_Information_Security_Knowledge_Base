# Ollama with NVIDIA GPU and Open WebUI using Docker Compose

This environment deploys **Ollama** and **Open WebUI** in two separate Docker containers.
Ollama gets access to the NVIDIA GPU. Open WebUI communicates with Ollama over an internal Docker network and is accessible via TCP port **3000**.

## Architecture

```text
Browser
   |
   | http://<XUBUNTU-IP>:3000
   v
+---------------------+
| Open WebUI          |
| Port 8080 in container
+----------+----------+
           |
           | Docker network ai_backend
           | http://ollama:11434
           v
+---------------------+
| Ollama              |
| NVIDIA GPU          |
| Port 11434 internal |
+---------------------+
```

In this configuration, Ollama port `11434` is intentionally **not published on the Xubuntu host**. This means the Ollama API is only reachable by containers connected to the Docker network.

---

## 1. Prerequisites

A current Xubuntu release based on a supported Ubuntu version is recommended, for example Ubuntu/Xubuntu 24.04 or newer.

Required components:

- NVIDIA GPU supported by Ollama
- current NVIDIA driver installed on the Xubuntu host
- Docker Engine
- Docker Compose v2 (`docker compose`)
- NVIDIA Container Toolkit
- sufficient system memory, VRAM, and free disk space for the models you plan to use

Ollama supports NVIDIA GPUs on Linux with a suitable compute capability. The current Ollama documentation lists Compute Capability 5.0+ and NVIDIA driver version 531 or newer.

### Check the NVIDIA driver

```bash
nvidia-smi
```

The NVIDIA GPU and installed driver version should be displayed.

### Check Docker

```bash
docker --version
docker compose version
```

If Docker is not yet installed, it can be set up as described in the following section.

### Install Docker Engine

Install the required packages and set up the official Docker repository:

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

Install Docker Engine, the CLI, containerd, and the Buildx and Compose plugins:

```bash
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Test the installation:

```bash
sudo docker run hello-world
```

Optional: add the current user to the `docker` group so Docker commands can be run without `sudo`. A logout and login is required afterwards:

```bash
sudo usermod -aG docker $USER
```

Then check the installation again:

```bash
docker --version
docker compose version
```

---

## 2. Install the NVIDIA Container Toolkit

Install the required packages:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
```

Configure the NVIDIA repository:

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

Update the package lists and install the toolkit:

```bash
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```

Configure Docker for the NVIDIA Container Runtime:

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Test GPU access from Docker:

```bash
docker run --rm --gpus all ubuntu nvidia-smi
```

If the NVIDIA GPU is also displayed inside the test container, the GPU passthrough configuration is working correctly.

---

## 3. Prepare the project directory

Example:

```bash
mkdir -p ~/ollama-openwebui
cd ~/ollama-openwebui
```

Copy the `docker-compose.yml` file into this directory.

The directory structure should then look similar to this:

```text
~/ollama-openwebui/
├── docker-compose.yml
└── README_EN.md
```

---

## 4. Create the Open WebUI Secret Key

Open WebUI should run with a persistent `WEBUI_SECRET_KEY`. The key is used, among other things, for signing sessions and should not change after a restart or when the container is recreated.

First, generate a random key with OpenSSL:

```bash
openssl rand -hex 32
```

Example output:

```text
8d2c71a2f4c95f0d8c1b6e4f0b6c2e0a9f7a13d4b8c6e1f275f6348af8df90bc
```

Create a `.env` file in the project directory:

```bash
nano .env
```

Add the generated key:

```text
WEBUI_SECRET_KEY=INSERT_THE_GENERATED_KEY_HERE
```

Alternatively, you can create the `.env` file directly in one step:

```bash
printf 'WEBUI_SECRET_KEY=%s\n' "$(openssl rand -hex 32)" > .env
chmod 600 .env
```

The directory structure should then look similar to this:

```text
~/ollama-openwebui/
├── .env
├── docker-compose.yml
└── README_EN.md
```

> The `.env` file contains a secret and should not be committed to a public Git repository or shared with others.

The Compose file reads the key with:

```yaml
environment:
  WEBUI_SECRET_KEY: ${WEBUI_SECRET_KEY}
```

---

## 5. Download the container images

```bash
docker compose pull
```

The following images are used:

- `ollama/ollama:latest`
- `ghcr.io/open-webui/open-webui:v0.11.1`

For production environments, it is recommended to use fixed image versions after successful testing instead of moving tags such as `latest` or `main`.

---

## 6. Start the environment

```bash
docker compose up -d
```

Check the status:

```bash
docker compose ps
```

Both containers should be shown as running:

```text
ollama
open-webui
```

Show the logs:

```bash
docker compose logs -f
```

Ollama only:

```bash
docker compose logs -f ollama
```

Open WebUI only:

```bash
docker compose logs -f open-webui
```

---

## 7. Install the first Ollama model

A model is downloaded directly inside the Ollama container. Example using `llama3.2`:

```bash
docker compose exec ollama ollama pull llama3.2
```

List installed models:

```bash
docker compose exec ollama ollama list
```

Run the model interactively in the terminal for testing:

```bash
docker compose exec ollama ollama run llama3.2
```

Exit the interactive Ollama session with `Ctrl+D`.

---

## 8. Access Open WebUI in a browser

### Access directly from the Xubuntu system

```text
http://localhost:3000
```

### Access from another computer on the network

Display the IP address of the Xubuntu system:

```bash
hostname -I
```

Then open, for example:

```text
http://192.168.1.50:3000
```

Replace `192.168.1.50` with the actual IP address of the Xubuntu system.

When Open WebUI is opened for the first time, the first user account is normally created. This first account receives administrative privileges.

If a firewall is active on Xubuntu, TCP port `3000` must be allowed for the required source networks. Example for a local network using UFW:

```bash
sudo ufw allow from 192.168.1.0/24 to any port 3000 proto tcp
```

Adjust the network address to match your own environment.

> For production use or when Open WebUI is exposed to the Internet, do not publish it unencrypted directly on port 3000. Use a reverse proxy with HTTPS and appropriate access controls.

---

## 9. Open WebUI connection to Ollama

The connection is configured automatically in `docker-compose.yml`:

```yaml
environment:
  OLLAMA_BASE_URL: http://ollama:11434
  ENABLE_OLLAMA_API: "True"
```

`ollama` is the Docker service name. Docker automatically provides name resolution within the shared `ai_backend` network.

The Ollama port is exposed only internally with `expose` and is not published on the host with `ports`.

---

## 10. Verify GPU usage

First, send a request to an Ollama model from Open WebUI or start a model using the CLI.

Then run the following on the Xubuntu host:

```bash
nvidia-smi
```

Ollama can also show whether a loaded model is running on CPU or GPU:

```bash
docker compose exec ollama ollama ps
```

In the `PROCESSOR` column, `100% GPU`, for example, means that the model has been loaded completely into GPU memory. If there is not enough VRAM, Ollama may split the model between CPU and GPU.

---

## 11. Stop and start the containers

Stop the containers:

```bash
docker compose stop
```

Start them again:

```bash
docker compose start
```

Remove the containers but keep persistent data:

```bash
docker compose down
```

The models and Open WebUI data remain stored in Docker volumes.

---

## 12. Update the environment

Download newer container images:

```bash
docker compose pull
```

Recreate the containers using the updated images:

```bash
docker compose up -d
```

Optionally remove unused images afterwards:

```bash
docker image prune
```

For production installations, new versions should first be tested and image tags should be versioned deliberately.

---

## 13. Persistent data

The Compose file uses two named Docker volumes:

```text
ollama_data       -> Ollama models and Ollama data
open_webui_data   -> users, settings, chats, and Open WebUI data
```

List Docker volumes:

```bash
docker volume ls
```

> Warning: `docker compose down -v` also deletes the persistent volumes and therefore removes downloaded Ollama models and Open WebUI data.

---

## 14. Useful commands

```bash
# Status
docker compose ps

# All logs
docker compose logs -f

# List models
docker compose exec ollama ollama list

# Download a model
docker compose exec ollama ollama pull llama3.2

# Show loaded models and CPU/GPU usage
docker compose exec ollama ollama ps

# Restart Ollama
docker compose restart ollama

# Restart Open WebUI
docker compose restart open-webui

# Restart the complete environment
docker compose restart
```

---

## 15. Troubleshooting

### Docker does not detect the NVIDIA GPU

Run the following test:

```bash
docker run --rm --gpus all ubuntu nvidia-smi
```

If this command fails, check the NVIDIA driver and NVIDIA Container Toolkit first.

### Ollama uses only the CPU

Check:

```bash
nvidia-smi
docker compose logs ollama
docker compose exec ollama ollama ps
```

For GPU detection issues, Ollama also recommends keeping NVIDIA drivers up to date and first ensuring that the Docker GPU test with `nvidia-smi` works correctly.

### Open WebUI does not show any Ollama models

Check whether the model is installed:

```bash
docker compose exec ollama ollama list
```

Check whether both containers are running:

```bash
docker compose ps
```

Check the Ollama and Open WebUI logs:

```bash
docker compose logs ollama
docker compose logs open-webui
```

The configured Ollama address inside the Docker network must be `http://ollama:11434`.

---

## Official Documentation

- Ollama Docker: https://docs.ollama.com/docker
- Ollama GPU Support: https://docs.ollama.com/gpu
- Ollama FAQ: https://docs.ollama.com/faq
- Open WebUI Quick Start: https://docs.openwebui.com/getting-started/quick-start/
- Open WebUI Environment Variables: https://docs.openwebui.com/reference/env-configuration/
- NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
- Docker Compose GPU Support: https://docs.docker.com/compose/how-tos/gpu-support/
