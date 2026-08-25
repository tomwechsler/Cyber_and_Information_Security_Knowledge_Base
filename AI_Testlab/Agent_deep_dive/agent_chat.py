# Local Ollama-based agent chat example.
# This script installs the required dependencies automatically, checks that Ollama
# is available locally, and runs a tool-enabled chat loop against a local model.

import os
import shutil
import subprocess
import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


def ensure_requirements() -> None:
    """Install missing Python packages required for a local LangChain + Ollama setup."""
    required_packages = [
        "langchain",
        "langchain-core",
        "langgraph",
        "langchain-ollama",
        "python-dotenv",
    ]

    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])

    if not shutil.which("ollama"):
        raise RuntimeError(
            "Ollama was not found in PATH. Install it from https://ollama.com and make sure "
            "the 'ollama' command works before running this script."
        )


def ensure_ollama_model(model_name: str) -> str:
    """Ensure the requested model is available locally; pull it if not."""
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"Unable to query local Ollama models: {result.stderr.strip() or result.stdout.strip()}"
        )

    installed = set()
    for line in result.stdout.strip().splitlines()[1:]:
        if line.strip():
            installed.add(line.split()[0])

    if model_name not in installed:
        print(f"Model '{model_name}' is not installed locally. Pulling it now...")
        subprocess.check_call(["ollama", "pull", model_name])

    return model_name


ensure_requirements()
load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")
ensure_ollama_model(OLLAMA_MODEL)

llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=0.2,
    base_url="http://localhost:11434",
)


@tool
def get_current_time() -> str:
    """Return the current local time in a readable format."""
    import datetime

    return datetime.datetime.now().strftime("%H:%M:%S")


@tool
def search_wikipedia(query: str) -> str:
    """Look up a brief summary for a topic using Wikipedia."""
    try:
        from wikipedia import summary

        return summary(query, sentences=2)
    except Exception:
        return "I couldn't find a reliable summary for that topic."


agent = create_agent(
    model=llm,
    tools=[get_current_time, search_wikipedia],
    system_prompt=(
        "You are a helpful assistant. Use the available tools when needed and keep responses concise."
    ),
)

conversation = [
    SystemMessage(
        content=(
            "You are a helpful AI assistant. Use the provided tools when they are useful, "
            "and keep your answers brief but informative."
        )
    )
]

print("Type 'exit' to quit.")
while True:
    user_input = input("User: ")
    if user_input.strip().lower() in {"exit", "quit"}:
        break

    conversation.append(HumanMessage(content=user_input))
    response = agent.invoke({"messages": conversation})
    assistant_message = response["messages"][-1]
    print("Bot:", assistant_message.content)
    conversation.append(AIMessage(content=assistant_message.content))
