# When AI Meets Security Controls: The Ethical Risks of Augmenting Cybersecurity with LLMs

Artificial Intelligence is rapidly transforming cybersecurity. From threat detection to automated analysis, AI promises efficiency, scalability, and deeper insights.

But what happens when **AI is combined with security technologies—and used unethically?**

This question is no longer theoretical.

As powerful tools such as local Large Language Models (LLMs) become widely accessible, the line between **defensive innovation and offensive misuse** is becoming increasingly blurred.

---

## The Convergence of AI and Security Technologies

Modern security tools such as **Web Application Firewalls (WAFs)** rely on rule-based detection mechanisms to protect applications against common threats.

Two widely recognized initiatives in this space are:

- **OWASP ModSecurity** – an open-source WAF engine  
- **OWASP Core Rule Set (CRS)** – a standardized set of detection rules  

These tools are designed to **detect and prevent attacks such as SQL injection, cross-site scripting (XSS), and other web-based threats**.

Traditionally, analyzing and improving such rule sets required deep expertise and manual effort.

Today, this is changing.

---

## The Rise of Local AI: Ollama and Open WebUI

With tools like:

- **Ollama** – a local large language model runtime  
- **Open WebUI** – an interface for interacting with local LLMs  

it is now possible to run powerful LLMs locally and interact with them in a controlled environment.

These models can:

- Analyze large rule sets such as OWASP CRS  
- Explain complex detection logic  
- Suggest improvements or optimizations  
- Simulate attack scenarios  

At first glance, this appears to be a **major advancement for defenders**.

And it is.

But it also introduces a new class of risks.

---

## When Defensive Tools Become Offensive Enablers

By combining LLMs with security rule sets, it becomes possible to:

- Systematically analyze detection rules  
- Identify weaknesses or gaps in coverage  
- Generate payloads designed to bypass protections  
- Optimize attack strategies using AI-assisted reasoning  

With **prompt engineering techniques**, users can instruct an LLM to:

> “Analyze this CRS rule and identify potential bypass techniques.”

What previously required expert-level knowledge can now be **partially automated and scaled**.

This creates a fundamental dilemma:

👉 The same tools that strengthen defense can also **lower the barrier for attackers**.

---

## The Ethical Dimension of AI in Cybersecurity

This is not just a technical issue—it is an ethical one.

### 1. Dual-Use Technology
AI in cybersecurity is inherently dual-use.  
The same capabilities can be used for **defense or exploitation**.

### 2. Democratization of Advanced Capabilities
Local AI tools make powerful analysis accessible to a much wider audience—including those with malicious intent.

### 3. Responsibility of Security Professionals
Security experts must decide **how far to go when testing systems**, especially when AI amplifies their capabilities.

### 4. Lack of Guardrails in Local Environments
Unlike cloud-based AI systems, local LLMs often operate without enforced restrictions or monitoring.

---

## A Practical Scenario: AI-Assisted CRS Analysis

Imagine a local setup where:

- OWASP CRS rules are loaded into an LLM  
- The model is queried using structured prompts  
- The output identifies potential weaknesses or edge cases  

This can be used to:

✅ Improve rule coverage  
✅ Enhance detection logic  
✅ Identify false positives  

But also:

❌ Discover bypass techniques  
❌ Generate evasive payloads  
❌ Test exploitation strategies at scale  

The difference lies not in the technology—but in **intent and governance**.

---

## Why This Matters Now

We are entering a phase where:

- AI capabilities are becoming **commoditized**  
- Security tools are increasingly **open and transparent**  
- Attackers are adopting AI at the same pace as defenders  

This convergence creates a new reality:

👉 **Security through obscurity is no longer viable**  
👉 **Understanding your defenses is now easier—for everyone**

---

## Managing the Risk: What Should Organizations Do?

To address these challenges, organizations should:

### 🔐 Establish Ethical Guidelines
Define clear policies for the use of AI in security testing and research.

### 🧪 Control AI Experimentation Environments
Ensure local AI labs are governed, monitored, and isolated.

### 📊 Strengthen Detection Through Diversity
Avoid relying solely on static rule sets—combine multiple detection approaches.

### 👥 Invest in Security Awareness
Educate teams on both the **capabilities and risks of AI-assisted security analysis**.

### 🔄 Continuously Update Security Controls
Assume that attackers are actively analyzing your defenses—and adapt accordingly.

---

## The Role of the Security Community

Projects like OWASP exist to **improve collective security**.

However, as AI accelerates analysis capabilities, the community must also evolve:

- Sharing knowledge responsibly  
- Anticipating misuse scenarios  
- Designing more resilient detection mechanisms  

---

## Final Thoughts

The combination of AI and cybersecurity technologies represents both an **opportunity and a risk**.

Tools like OWASP ModSecurity, CRS, and local LLM environments can significantly enhance our ability to defend systems.

But they also make it easier to **analyze, understand, and potentially exploit those same defenses**.

The critical question is no longer:

👉 *“Can we do this?”*

But rather:

👉 *“Should we—and under what conditions?”*

---

**How do you approach the ethical use of AI in cybersecurity?**  
Where should organizations draw the line between research and risk?

> Source: My own analysis and experience in my own AI lab, combined with documents such as the [OWASP ModSecurity documentation](https://owasp.org/www-project-modsecurity/) and the [OWASP CRS documentation](https://coreruleset.org/). The ethical considerations are based on general principles of dual-use technology and responsible AI use.