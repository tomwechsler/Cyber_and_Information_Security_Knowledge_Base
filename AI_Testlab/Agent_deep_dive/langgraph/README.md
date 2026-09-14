# LangGraph Agent Examples

This folder contains three example agents built with [LangGraph](https://langchain-ai.github.io/langgraph/). They all use a local LLM served by [Ollama](https://ollama.com) (default model: `qwen2.5:14b`) so no API key is needed. Each script installs its own missing Python packages automatically when you run it.

The three scripts show three different *types* of agent, from simplest to most advanced.

---

## 1. `basic_example.py` — Decision / Routing Agent

**What it does:** Takes a URL, runs a mock "threat lookup" tool on it, then asks the LLM to classify the URL as `malicious` or `benign` and explain why. Based on that verdict, the graph branches to one of two end paths.

**How it works (in simple steps):**
1. `enrich_url` node — calls a fake lookup tool (`analyze_url_tool`) that returns a canned threat level for a few hardcoded domains.
2. `ai_triage` node — sends the lookup result to the LLM, which returns a structured JSON verdict (`malicious`/`benign`) plus an explanation.
3. A **conditional edge** reads that verdict and routes to either a `report_malicious` or `report_benign` node.
4. The script runs this flow three times with different example URLs.

**Type of agent:** A **single-pass decision/routing agent**. It does not loop or use tools dynamically — it follows one fixed sequence (tool → LLM → branch → end). This is the simplest pattern LangGraph supports: a linear workflow with one conditional fork based on an LLM's classification.

---

## 2. `cisa_kev_agent.py` — Sequential Pipeline Agent

**What it does:** Downloads the 3 most recent entries from CISA's Known Exploited Vulnerabilities (KEV) catalog, then uses the LLM to summarize each vulnerability's impact and analyze how it could be exploited (including its likely CWE category), and finally prints a combined report.

**How it works (in simple steps):**
1. `fetch_vulnerabilities` node — downloads the live CISA KEV JSON feed and keeps the latest 3 entries.
2. `summarize_vulnerabilities` node — asks the LLM for a one-sentence "potential impact" summary per vulnerability.
3. `analyze_exploitation` node — asks the LLM for the likely CWE ID, a CWE explanation, and an attack-vector summary per vulnerability.
4. `report_results` node — merges everything into one readable report and prints it.

**Type of agent:** A **sequential (linear) pipeline agent** — sometimes called a workflow chain. There are no conditional branches and no loops; every node always runs in a fixed order, one after another. It's essentially an automated research/reporting pipeline where the LLM is used purely as a summarization/analysis step, not as a decision-maker.

---

## 3. `ethical_hacking_agent.py` — Tool-Calling ReAct Agent with Memory

**What it does:** Acts like a conversational cybersecurity assistant. It can decide on its own, based on the user's message, whether to run a real `nmap` port scan, search a (simulated) Exploit-DB for known exploits, or just reply directly — and it remembers the whole conversation across multiple turns.

**How it works (in simple steps):**
1. Two tools are defined: `nmap_tool` (runs a real Nmap scan via `python-nmap`) and `exploitdb_tool` (a mock Exploit-DB search).
2. The LLM is "bound" to these tools, meaning it can choose to call them itself instead of just answering in text.
3. The `agent` node calls the LLM with the conversation so far. A conditional edge (`should_continue`) checks: did the LLM just request a tool call? If yes, go to the `tools` node; if no, end the turn.
4. The `tools` node executes whichever tool the LLM asked for, and the result is fed back to the `agent` node so the LLM can use it to form its final answer.
5. A `MemorySaver` checkpointer keeps the full message history (`AgentState.messages`) alive between calls, identified by a `thread_id`. This is why the script can simulate a 4-turn conversation ("scan localhost" → "check for Apache exploits" → "how do I use that exploit?" → "give me mitigations") where each answer builds on the previous ones.

**Type of agent:** A classic **ReAct-style, tool-using conversational agent with persistent memory**. Unlike the other two scripts, this one has a genuine loop (`agent ⇄ tools`) that can repeat multiple times per turn, it decides dynamically which tool (if any) to use, and it keeps state across multiple separate invocations rather than running once and stopping.

---

## Summary Comparison

| Script | Agent type | Has branching? | Has loops? | Has memory across runs? | Uses real external tools? |
|---|---|---|---|---|---|
| `basic_example.py` | Decision/routing agent | Yes (1 fork) | No | No | No (mock tool) |
| `cisa_kev_agent.py` | Sequential pipeline agent | No | No | No | Yes (live CISA feed) |
| `ethical_hacking_agent.py` | ReAct tool-calling agent | Yes | Yes (agent↔tools) | Yes (checkpointer) | Yes (real Nmap scan) |

**Note:** `ethical_hacking_agent.py` runs real Nmap scans — only use it against systems you own or are authorized to test (the example scans `localhost`).
