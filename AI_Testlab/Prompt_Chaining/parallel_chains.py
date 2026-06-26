# We will create a parallel chain that combines two branches: reconnaissance and exploitation.
# The reconnaissance branch will generate a prompt for reconnaissance techniques and tools based on target information.
# The exploitation branch will generate a prompt for exploitation methods and tools based on target information.
# The two branches will be combined into a penetration testing plan.
# The final result will be printed.

# Import the required libraries
import os
import sys
import ollama as _ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_ollama import ChatOllama

OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:14b")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

def _check_ollama():
    try:
        client = _ollama.Client(host=OLLAMA_HOST)
        available = [m.model for m in client.list().models]
        if not any(OLLAMA_MODEL in m for m in available):
            print(f"Model '{OLLAMA_MODEL}' not found. Available: {available}")
            print(f"Run: ollama pull {OLLAMA_MODEL}")
            sys.exit(1)
    except Exception as e:
        print(f"Cannot connect to Ollama at {OLLAMA_HOST}: {e}")
        print("Install and start Ollama: https://ollama.com")
        sys.exit(1)

_check_ollama()

# Create a local Ollama model (qwen2.5:14b fits in 16GB VRAM at ~8.7GB)
model = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_HOST)

# Define prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert ethical hacker and penetration tester."),
        ("human", "Outline the main characteristics and potential entry points of the target system {target_system}."),
    ]
)

def perform_reconnaissance(target_info):
    '''
    This function generates a prompt for reconnaissance techniques and tools based on target information.
    args: target_info (str): Information about the target system
    returns: str: Prompt for reconnaissance techniques and tools
    '''
    recon_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert ethical hacker specializing in reconnaissance."),
            (
                "human",
                "Given this target information: {target_info}, list potential reconnaissance techniques and tools to gather more information.",
            ),
        ]
    )
    return recon_template.format_prompt(target_info=target_info)

# Define exploitation step
def plan_exploitation(target_info):
    '''
    This function generates a prompt for exploitation methods and tools based on target information.
    args: target_info (str): Information about the target system
    returns: str: Prompt for exploitation methods and tools
    '''
    exploit_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert ethical hacker specializing in exploitation techniques."),
            (
                "human",
                "Based on this target information: {target_info}, suggest potential exploitation methods and tools.",
            ),
        ]
    )
    return exploit_template.format_prompt(target_info=target_info)

# Combine reconnaissance and exploitation into a penetration testing plan
def create_pentest_plan(recon, exploit):
    '''
    This function combines the reconnaissance and exploitation phases into a penetration testing plan.
    args: recon (str): Reconnaissance phase output
          exploit (str): Exploitation phase output
          returns: str: Penetration testing plan
          '''
    return f"Reconnaissance Phase:\n{recon}\n\nExploitation Phase:\n{exploit}"

# Simplify branches with LCEL (LangChain Expression Language)
# Define the reconnaissance and exploitation branches
recon_branch_chain = (
    RunnableLambda(lambda x: perform_reconnaissance(x)) | model | StrOutputParser()
)
exploit_branch_chain = (
    RunnableLambda(lambda x: plan_exploitation(x)) | model | StrOutputParser()
)

# Create the combined chain using LCEL
# The chain consists of a prompt template, an OpenAI model, a string output parser, and two parallel branches for reconnaissance and exploitation.
chain = (
    prompt_template
    | model
    | StrOutputParser()
    | RunnableParallel(branches={"reconnaissance": recon_branch_chain, "exploitation": exploit_branch_chain})
    | RunnableLambda(lambda x: create_pentest_plan(x["branches"]["reconnaissance"], x["branches"]["exploitation"]))
)

# Run the chain with a target system as input
result = chain.invoke({"target_system": "E-commerce website running in the cloud"})

# Print the final result
print(result)