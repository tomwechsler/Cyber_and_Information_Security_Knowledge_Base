# Ubuntu Linux Environment
This document provides instructions for setting up an Ubuntu Linux environment for AI development and testing.

## 1. Install Ubuntu Linux
You can download the latest version of Ubuntu from the official website: [Ubuntu Downloads](https://ubuntu.com/download). Follow the installation instructions to set up Ubuntu on your machine.

## 2. Update and Upgrade
After installing Ubuntu, open a terminal and run the following commands to update and upgrade your system:

```bash
sudo apt update
sudo apt upgrade -y
```

## 3. Install Ollama
Ollama is a local large language model runtime that allows you to run powerful LLMs locally. To install Ollama, follow the instructions on their official website: [Ollama Installation](https://ollama.com/docs/installation).

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## 4. Install Python
Python is essential for AI development. Install Python and pip using the following command: 

```bash
sudo apt install python3 python3-pip -y
```

## 5. Set Up a Virtual Environment
It's recommended to use a virtual environment for your AI projects. You can create one using the following commands:    

```bash
python3 -m venv ai-env
source ai-env/bin/activate
```

## 6. Install Open WebUI
Open WebUI is an interface for interacting with local LLMs. To install Open WebUI, you can use pip:

```bash
pip install open-webui
```

```bash
open-webui serve
```

## 7. Test Your Setup
To verify that everything is set up correctly, you can run a simple test to check if Ollama and Open WebUI are working:

```bash
ollama --version
open-webui --version
```

If both commands return the version numbers without errors, your environment is ready for AI development and testing.