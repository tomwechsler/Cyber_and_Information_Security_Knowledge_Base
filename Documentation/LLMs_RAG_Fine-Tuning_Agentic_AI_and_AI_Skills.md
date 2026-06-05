# LLMs, RAG, Fine-Tuning, Agentic AI and AI Skills: From Language Models to Secure AI-Driven Cybersecurity Workflows

Artificial Intelligence is evolving rapidly.

Only a short time ago, many organizations were experimenting with Large Language Models as standalone chat interfaces. Today, we are moving toward AI systems that can retrieve knowledge, reason over internal data, use tools, orchestrate workflows, and support complex tasks in cybersecurity, IT operations, software development, and governance.

This evolution can be understood as a journey:

**LLMs → RAG → Fine-Tuning → Agentic AI → MCP → AI Skills**

Each step adds new capabilities. But each step also introduces new security, governance, and operational risks.

For cybersecurity professionals, this is especially important. AI can support threat analysis, incident response, vulnerability management, security awareness, and secure development. At the same time, AI systems can introduce new attack surfaces such as prompt injection, data leakage, insecure tool use, excessive agency, and supply chain risk.

The question is no longer:

**Can AI support cybersecurity?**

The better question is:

**How can we design AI-powered cybersecurity workflows that are useful, secure, governed, and trustworthy?**

━━━━━━━━━━━━━━━━━━━━

## 1. Large Language Models: The Foundation

Large Language Models, or LLMs, are AI models designed to understand, generate, summarize, classify, and reason over natural language.

They can support tasks such as:

- Explaining complex security concepts
- Summarizing incident reports
- Drafting policies and procedures
- Assisting with log analysis
- Generating training content
- Supporting security documentation
- Helping analysts understand alerts

In cybersecurity, this can be extremely valuable.

A security analyst may ask an LLM:

“Summarize this incident timeline and identify the most important indicators of compromise.”

A security architect may ask:

“Explain the risks of exposing this API endpoint to the internet.”

A trainer may ask:

“Create a short awareness module about phishing and MFA.”

LLMs are powerful because they make technical knowledge more accessible.

But they also have limitations.

━━━━━━━━━━━━━━━━━━━━

## The Limits of Standalone LLMs

A standalone LLM usually relies on knowledge learned during training and whatever information is included in the prompt.

That means it may not know:

- Your latest internal policies
- Your current network architecture
- Your organization’s incident response process
- Your recent SIEM alerts
- Your asset inventory
- Your specific cloud configuration
- Your current vulnerabilities
- Your business priorities

This creates several risks:

- Hallucinated answers
- Outdated recommendations
- Lack of organizational context
- Overconfident but incorrect responses
- Security guidance that sounds plausible but does not fit reality

In cybersecurity, this can be dangerous. A wrong recommendation during incident response may delay containment. A hallucinated compliance statement may mislead management. A generic security control recommendation may ignore business-critical dependencies. This is why many organizations quickly move from standalone LLMs to context-aware architectures.

That is where **Retrieval-Augmented Generation** comes in.

━━━━━━━━━━━━━━━━━━━━

## 2. Retrieval-Augmented Generation: Giving the Model Context

**Retrieval-Augmented Generation**, or **RAG**, is an architecture that connects an LLM to external knowledge sources. Instead of relying only on the model’s internal knowledge, RAG retrieves relevant information from data sources and adds it to the prompt as context.

A typical RAG workflow looks like this:

1. Documents, logs, policies, tickets, or knowledge articles are processed.
2. An embedding model converts content into numerical representations.
3. These embeddings are stored in a vector database.
4. A user asks a question.
5. Semantic search retrieves relevant content.
6. The retrieved context is added to the prompt.
7. The LLM generates an answer based on the prompt and context.

In simple terms:

**RAG helps the model answer with your data, not just its training data.**

━━━━━━━━━━━━━━━━━━━━

## Practical Cybersecurity Example: Policy Assistant

Imagine an organization has hundreds of pages of security policies, standards, baselines, and procedures.

Employees ask questions such as:

- “Can I use a personal device for remote work?”
- “What is the password standard for privileged accounts?”
- “How do I report a suspected phishing email?”
- “Which data classification requires encryption?”

A RAG-based assistant can retrieve the relevant policy sections and generate a clear answer.

This improves:

- Access to security knowledge
- Consistency of answers
- Employee awareness
- Policy adoption
- Help desk efficiency

But this only works well if the underlying knowledge base is accurate, current, and properly access-controlled.

━━━━━━━━━━━━━━━━━━━━

## Practical Cybersecurity Example: Incident Response Knowledge Assistant

A SOC team can use RAG to connect an LLM to:

- Incident response playbooks
- Previous incident reports
- SIEM alert documentation
- MITRE ATT&CK mappings
- Internal escalation procedures
- Asset criticality data
- Contact lists and communication templates

When an incident occurs, an analyst may ask:

“What are the recommended containment steps for suspected credential theft affecting privileged accounts?”

The system can retrieve the relevant playbook and produce a structured response. This can reduce response time. But the analyst must still validate the output. RAG supports decision-making. It should not blindly replace it.

━━━━━━━━━━━━━━━━━━━━

## RAG vs. Fine-Tuning

RAG and fine-tuning are often confused. They solve different problems.

**RAG** connects a model to external knowledge.

**Fine-tuning** changes the model’s behavior by training it further on specific examples.

A simplified comparison:

**RAG is useful when:**

- Knowledge changes frequently
- You need access to internal documents
- You want current information
- You want lower cost than retraining
- You need source-grounded answers
- You want easier updates

**Fine-tuning is useful when:**

- You need a model to perform a specialized task
- You want consistent style or behavior
- You need domain-specific classification
- The task is stable and repeatable
- You have high-quality training data

For cybersecurity, RAG is often the better starting point because security knowledge changes constantly.

- Threats change.
- Vulnerabilities change.
- Policies change.
- Cloud environments change.
- Incident response playbooks change.

A RAG system can update knowledge without retraining the model.

━━━━━━━━━━━━━━━━━━━━

## 3. Fine-Tuning: Teaching the Model a Specialized Behavior

Fine-tuning means further training a model on specific examples so that it performs better on a targeted task.

In cybersecurity, fine-tuning can be useful for:

- Classifying phishing emails
- Categorizing incident tickets
- Identifying log patterns
- Producing standardized report formats
- Detecting specific types of security language
- Supporting domain-specific workflows

For example, a company could fine-tune a model to classify security tickets into categories such as:

- Phishing
- Malware
- Data leakage
- Access violation
- Suspicious login
- Vulnerability report
- Policy exception

Fine-tuning can improve consistency for specialized tasks. But it also introduces challenges.

━━━━━━━━━━━━━━━━━━━━

## Risks and Challenges of Fine-Tuning

Fine-tuning requires careful governance.

Important questions include:

- What data is used for training?
- Does the data contain sensitive information?
- Is the data representative?
- Could the model learn unwanted patterns?
- How is performance measured?
- How is bias evaluated?
- How is the model versioned?
- How is rollback handled?
- How is the fine-tuned model tested against misuse?

Fine-tuning can also become expensive and operationally complex. It may require retraining when data changes. It may still hallucinate when facing unfamiliar inputs. And if the training data contains errors, the model may learn those errors.

For many organizations, the practical approach is:

**Use RAG for knowledge. Use fine-tuning for behavior.**

━━━━━━━━━━━━━━━━━━━━

## Practical Cybersecurity Example: RAG and Fine-Tuning Together

A security team wants an AI assistant for incident triage.

RAG can provide:

- Current playbooks
- Internal escalation paths
- Asset criticality
- Recent threat intelligence
- Known vulnerabilities
- Previous incident reports

Fine-tuning can help the model:

- Classify incidents consistently
- Use the organization’s reporting style
- Apply standard severity language
- Produce structured summaries

Together, they create a stronger system. RAG provides context. Fine-tuning provides task-specific behavior.

━━━━━━━━━━━━━━━━━━━━

## 4. From Assistants to Agents: What Is Agentic AI?

Agentic AI goes beyond answering questions. An AI agent can plan, use tools, call APIs, retrieve information, execute steps, and adapt based on results.

A simple chatbot might answer:

“Here are recommended steps for investigating suspicious login activity.”

An agentic system might:

1. Receive a suspicious login alert.
2. Query identity logs.
3. Check geo-location anomalies.
4. Search for related alerts.
5. Query endpoint activity.
6. Summarize findings.
7. Recommend containment actions.
8. Open a ticket.
9. Notify an analyst.

This is a major shift. The AI system is no longer only generating text. It is participating in a workflow.

━━━━━━━━━━━━━━━━━━━━

## Agentic AI in Cybersecurity

Agentic AI can support many cybersecurity use cases:

- SOC alert enrichment
- Threat intelligence collection
- Vulnerability prioritization
- Incident response assistance
- Phishing analysis
- Malware triage support
- Security policy review
- Cloud configuration analysis
- Compliance evidence collection
- Security awareness content generation
- Attack path analysis

### Practical Example: Phishing Investigation Agent

A phishing investigation agent could:

- Analyze the email body
- Extract URLs and attachments
- Check sender reputation
- Query threat intelligence
- Search for similar emails
- Identify affected users
- Recommend containment steps
- Draft a user notification
- Create an incident ticket

This can significantly reduce analyst workload. But it also introduces risk.

- What if the agent blocks the wrong sender?
- What if it deletes legitimate emails?
- What if it leaks sensitive investigation data?
- What if a malicious email uses prompt injection to manipulate the agent?

This is why agentic AI requires **strong controls**.

━━━━━━━━━━━━━━━━━━━━

## The Cybersecurity Risk of Agentic AI

Agentic systems increase both capability and risk.

Key risks include:

- Excessive permissions
- Unsafe tool execution
- Prompt injection
- Sensitive data exposure
- Unverified outputs
- Insecure integrations
- Poor logging
- Lack of human approval
- Agent-to-agent error propagation
- Automation of wrong actions
- Abuse by attackers
- Supply chain compromise of tools or connectors

The OWASP Top 10 for LLM and Generative AI applications identifies major risks such as prompt injection, sensitive information disclosure, insecure plugin design, excessive agency, overreliance, model theft, supply chain vulnerabilities, and other GenAI application risks. ([OWASP][1])

For agentic AI, “excessive agency” is especially important. The more an AI system can do, the more carefully its permissions and actions must be controlled.

━━━━━━━━━━━━━━━━━━━━

## 5. Model Context Protocol: Standardizing Tool and Data Access

As agents become more capable, they need access to tools and data. Traditionally, every AI application needed custom integrations for databases, APIs, files, search systems, development tools, productivity platforms, and business applications. This does not scale well.

The **Model Context Protocol**, or **MCP**, addresses this problem by providing a standardized way for AI applications to connect to external systems. MCP is described by its official documentation as an open-source standard for connecting AI applications to external systems such as data sources, tools, and workflows. ([Model Context Protocol][2])

Anthropic introduced MCP in November 2024 as an open standard for connecting AI assistants to systems where data lives, including content repositories, business tools, and development environments. ([Anthropic][3])

A common analogy is:

**MCP is like a USB-C port for AI applications.**

It creates a standardized interface between AI applications and external capabilities.

━━━━━━━━━━━━━━━━━━━━

## Practical Cybersecurity Example: MCP for SOC Workflows

An AI security assistant could use MCP servers to connect to:

- SIEM queries
- Ticketing systems
- Threat intelligence platforms
- Asset inventory
- Vulnerability scanners
- EDR systems
- Documentation repositories
- Cloud security tools

Instead of building a custom integration for each tool and each AI application, MCP can provide a more standardized approach.

Example workflow:

1. Analyst asks: “Investigate this suspicious login.”
2. Agent queries identity logs through an MCP server.
3. Agent checks endpoint telemetry.
4. Agent retrieves asset criticality.
5. Agent searches previous incidents.
6. Agent summarizes findings.
7. Analyst approves containment action.

This can make cybersecurity operations more efficient. But it must be designed securely.

━━━━━━━━━━━━━━━━━━━━

## Security Considerations for MCP

MCP improves interoperability, but it also expands the attack surface.

Important security questions include:

- Which tools can the AI access?
- What permissions does each MCP server have?
- Is authentication strong?
- Is authorization granular?
- Are tool calls logged?
- Can prompts influence unsafe tool execution?
- Are outputs validated before action?
- Is there human approval for high-risk actions?
- Are MCP servers isolated?
- Are secrets protected?
- Are third-party MCP servers reviewed?

In cybersecurity environments, MCP should follow Zero Trust principles. Do not assume trust simply because a tool is connected.

- Verify identity
- Limit permissions
- Monitor activity
- Log every action (if possible)

Require **approval** for sensitive operations.

━━━━━━━━━━━━━━━━━━━━

## 6. Agent Skills: Packaging Specialized Capabilities

As agents become more sophisticated, they need reusable skills.

**Agent Skills** are a way to package specialized knowledge, workflows, instructions, scripts, templates, and resources so an agent can perform specific tasks more reliably.

The official Agent Skills documentation describes Agent Skills as a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows. At its core, a skill is a folder containing a `SKILL.md` file with metadata and instructions, and it can also bundle scripts, references, templates, and other resources. ([agentskills.io][4])

Claude’s official documentation similarly describes Agent Skills as modular capabilities that package instructions, metadata, and optional resources that the model can use automatically when relevant. ([Claude Plattform][5])

A key concept is **progressive disclosure**. The agent does not need to load all instructions all the time. It can first discover that a skill exists, then activate it when relevant, and finally execute the detailed instructions or use bundled resources.

━━━━━━━━━━━━━━━━━━━━

## Practical Cybersecurity Example: Incident Response Skill

An “Incident Response Skill” could include:

- Triage checklist
- Severity classification guidance
- Communication templates
- Evidence collection steps
- Containment decision tree
- Legal and compliance escalation rules
- Report template
- Links to playbooks
- Scripts for log collection

When the agent detects that the user is working on an incident, it activates the skill. This allows the agent to support a standardized workflow.

### Example User Request

“We have a suspected credential compromise. Help me structure the response.”

The agent could use the Incident Response Skill to produce:

- Initial triage questions
- Containment checklist
- Evidence preservation steps
- Stakeholder communication draft
- Recommended next actions
- Post-incident review structure

This is much more reliable than asking a generic LLM.

━━━━━━━━━━━━━━━━━━━━

## Practical Cybersecurity Example: Secure Code Review Skill

A Secure Code Review Skill could include:

- OWASP Top 10 guidance
- Secure coding checklist
- Language-specific rules
- Common vulnerability patterns
- Example remediation snippets
- Secure review report template
- SAST tool integration instructions

A developer could ask:

“Review this authentication function for security weaknesses.”

The agent uses the skill to structure its review and produce consistent findings. This supports secure development and aligns well with secure software development practices.

━━━━━━━━━━━━━━━━━━━━

## Practical Cybersecurity Example: Compliance Evidence Skill

A Compliance Evidence Skill could help collect and structure evidence for:

- ISO/IEC 27001 audits
- SOC 2 controls
- NIST CSF assessments
- Internal security reviews
- AI governance reviews
- Access control evidence
- Backup testing evidence
- Security awareness training records

The skill might include:

- Evidence checklist
- Interview questions
- Document templates
- Control mapping guidance
- Report structure

This can reduce manual work and improve consistency. But access to evidence repositories must be tightly controlled.

━━━━━━━━━━━━━━━━━━━━

## Chronological View: How the Pieces Fit Together

The evolution can be understood like this:

### Stage 1: LLM

The model can understand and generate language.

Cybersecurity value:

- Explanation
- Summarization
- Drafting
- Basic analysis

Main risk:

- Hallucination and lack of context

### Stage 2: RAG

The model can retrieve relevant external knowledge.

Cybersecurity value:

- Policy assistants
- Incident playbook retrieval
- Knowledge-based SOC support
- Internal documentation search

Main risk:

- Data leakage, poor retrieval quality, access control failures

### Stage 3: Fine-Tuning

The model learns specialized behavior.

Cybersecurity value:

- Classification
- Standardized reporting
- Domain-specific analysis
- Consistent outputs

Main risk:

- Training data quality, privacy, bias, model governance

### Stage 4: Agentic AI

The system can plan and use tools.

Cybersecurity value:

- Workflow automation
- Alert enrichment
- Threat investigation
- Vulnerability prioritization
- Incident response support

Main risk:

- Excessive agency, unsafe actions, insecure tool use

### Stage 5: MCP

The agent connects to tools and data through a standardized protocol.

Cybersecurity value:

- Scalable integrations
- Tool interoperability
- More flexible AI workflows

Main risk:

- Connector security, tool permissions, supply chain exposure

### Stage 6: Agent Skills

The agent gains reusable domain-specific capabilities.

Cybersecurity value:

- Standardized workflows
- Repeatable tasks
- Role-specific expertise
- Better operational consistency

Main risk:

- Skill supply chain risk, unsafe instructions, excessive permissions, weak review processes

━━━━━━━━━━━━━━━━━━━━

## Frameworks and Standards for Secure AI Adoption

AI-powered cybersecurity workflows should not be built without governance. Several frameworks and standards can help.

━━━━━━━━━━━━━━━━━━━━

## NIST AI RMF

The NIST AI Risk Management Framework helps organizations manage risks to individuals, organizations, and society associated with AI systems. NIST describes the AI RMF as a framework developed to better manage AI-related risks. ([NIST][6])

For LLMs, RAG, agents, MCP, and skills, the NIST AI RMF can help structure:

- Governance
- Context mapping
- Risk measurement
- Risk treatment
- Continuous monitoring

It is especially useful for ensuring that AI systems are valid, reliable, safe, secure, resilient, transparent, explainable, privacy-enhanced, and fair.

━━━━━━━━━━━━━━━━━━━━

## ISO/IEC 42001

ISO/IEC 42001 supports the establishment of an AI Management System. It is useful for organizations that want formal governance around AI.

It can help define:

- AI policies
- Roles and responsibilities
- Risk processes
- Documentation
- Internal audits
- Continuous improvement

For agentic AI, ISO/IEC 42001 is valuable because it helps turn experimentation into managed organizational practice.

━━━━━━━━━━━━━━━━━━━━

## ISO/IEC 23894

ISO/IEC 23894 provides guidance for AI risk management.

It can support:

- AI risk identification
- AI risk analysis
- AI risk evaluation
- Risk treatment
- Monitoring and review

This is highly relevant when assessing RAG systems, fine-tuned models, AI agents, and AI-enabled cybersecurity workflows.

━━━━━━━━━━━━━━━━━━━━

## NIST Cybersecurity Framework

The NIST Cybersecurity Framework supports cybersecurity risk management across governance, identification, protection, detection, response, and recovery.

For AI systems, it helps answer questions such as:

- How is access controlled?
- How are systems monitored?
- How are incidents detected?
- How are AI systems recovered?
- How are third-party dependencies managed?

AI systems are still systems. They need cybersecurity controls.

━━━━━━━━━━━━━━━━━━━━

## OWASP Top 10 for LLM Applications

The OWASP Top 10 for LLM Applications is highly relevant for secure LLM and agentic application development. OWASP describes the project as identifying critical security vulnerabilities in LLM applications, and the GenAI Security Project provides the latest LLM and GenAI risks and mitigations. ([OWASP][1])

Important risks include:

- Prompt injection
- Sensitive information disclosure
- Insecure output handling
- Excessive agency
- Supply chain vulnerabilities
- Insecure plugin or tool design
- Model denial of service
- Overreliance

These risks should be explicitly considered when designing RAG and agentic cybersecurity systems.

━━━━━━━━━━━━━━━━━━━━

## MITRE ATLAS

MITRE ATLAS is useful for understanding adversarial threats against AI-enabled systems.

It can help teams think about:

- Data poisoning
- Model evasion
- Model extraction
- Abuse of AI behavior
- Attacks against ML pipelines
- AI-specific incident scenarios

For cybersecurity teams, MITRE ATLAS supports AI threat modeling and AI red teaming.

━━━━━━━━━━━━━━━━━━━━

## NIST SP 800-53, SP 800-61 and SP 800-218

Traditional cybersecurity standards are still relevant.

### NIST SP 800-53

Useful for selecting security and privacy controls.

### NIST SP 800-61

Useful for incident response planning and AI-related incident procedures.

### NIST SP 800-218 Secure Software Development Framework

Useful when AI systems, MCP servers, plugins, tools, and agent skills are developed internally. AI security is not separate from secure engineering. It must be part of the same lifecycle.

━━━━━━━━━━━━━━━━━━━━

## Key Security Principles for LLMs, RAG, Agents and Skills

Organizations should apply several practical principles.

### 1. Least Privilege

Agents should only access the tools and data required for the task.

### 2. Human-in-the-Loop

High-impact actions should require human approval.

### 3. Secure Retrieval

RAG systems must enforce access control during retrieval.

### 4. Prompt Injection Defense

Inputs, retrieved content, and tool outputs should be treated as untrusted.

### 5. Logging and Auditability

Prompt history, retrieval events, tool calls, and agent actions should be logged.

### 6. Data Classification

Sensitive data should be protected before entering AI workflows.

### 7. Output Validation

AI-generated recommendations should be reviewed before execution.

### 8. Model and Skill Governance

Models, prompts, skills, and tools should be versioned, reviewed, and approved.

### 9. Supply Chain Security

External models, plugins, skills, MCP servers, and datasets should be assessed.

### 10. Incident Response

Organizations need procedures for AI-specific incidents.

Examples include:

- Prompt injection
- Data leakage
- Unauthorized tool execution
- Compromised MCP server
- Unsafe agent action
- Malicious skill package
- Model behavior drift

━━━━━━━━━━━━━━━━━━━━

## Practical End-to-End Example: AI SOC Assistant

A mature AI SOC assistant could combine several components.

### LLM

Summarizes alerts and explains findings.

### RAG

Retrieves incident playbooks, asset context, previous cases, and threat intelligence.

### Fine-Tuning

Improves classification of incidents and severity ratings.

### Agentic AI

Queries tools, enriches alerts, opens tickets, and drafts reports.

### MCP

Standardizes connections to SIEM, EDR, ticketing, asset inventory, and vulnerability scanners.

### Agent Skills

Provides reusable workflows for phishing triage, ransomware response, credential compromise, and executive reporting.

### Security Controls

- Analyst approval for containment
- Read-only access by default
- Tool call logging
- Role-based access
- Prompt injection testing
- Retrieval access control
- Secure skill review
- Incident response process

This is where AI becomes operationally valuable. But only if governance and security are built in from the start.

━━━━━━━━━━━━━━━━━━━━

## Practical End-to-End Example: AI Vulnerability Management Assistant

A vulnerability management assistant could:

- Retrieve asset criticality
- Check exploit availability
- Correlate vulnerabilities with exposure
- Summarize remediation guidance
- Generate patch priority lists
- Create tickets
- Notify system owners

RAG provides current asset and vulnerability context. Agentic AI performs workflow steps. MCP connects the assistant to scanners, CMDB, ticketing, and documentation. Agent Skills standardize vulnerability triage workflows.

The key risk:

The assistant could prioritize incorrectly if data quality is poor.

Therefore, control measures should include:

- Validation against asset inventory
- Human approval for critical decisions
- Risk scoring transparency
- Audit logs
- Clear ownership
- Regular performance review

━━━━━━━━━━━━━━━━━━━━

## Practical End-to-End Example: Secure Development Assistant

A secure development assistant could:

- Review code for vulnerabilities
- Retrieve internal secure coding standards
- Reference OWASP guidance
- Generate test cases
- Identify hardcoded secrets
- Suggest safer implementation patterns
- Create remediation tickets

RAG connects the model to internal standards. Fine-tuning improves review consistency. Agent Skills package secure code review procedures. MCP connects the assistant to repositories, issue trackers, and scanning tools.

Important controls include:

- No automatic code merge
- Human review required
- Secrets redaction
- Dependency scanning
- Secure coding policy enforcement
- Logging of recommendations
- Developer training

AI can accelerate secure development. But it must not bypass secure engineering discipline.

━━━━━━━━━━━━━━━━━━━━

## What Many Organizations Miss

Organizations often focus on the model and forget the system around it.

Important missing elements include:

### 1. AI Inventory

Know where LLMs, RAG systems, agents, MCP servers, and skills are used.

### 2. Data Governance

Know what data is used, where it comes from, and who may access it.

### 3. Access Control for Retrieval

RAG must not retrieve documents the user is not authorized to see.

### 4. Tool Permission Boundaries

Agents should not have broad administrative privileges.

### 5. Skill Review Process

Agent Skills should be reviewed like code and security playbooks.

### 6. MCP Server Governance

MCP servers should be inventoried, hardened, monitored, and version-controlled.

### 7. AI Incident Response

Prepare for prompt injection, leakage, unsafe tool execution, and agent malfunction.

### 8. Evaluation and Testing

Continuously test accuracy, robustness, safety, and security.

### 9. User Training

Users must understand what AI can and cannot do.

### 10. Metrics

Measure effectiveness, error rates, unsafe outputs, response times, and business impact.

━━━━━━━━━━━━━━━━━━━━

## Final Thoughts

LLMs are powerful. RAG makes them context-aware. Fine-tuning makes them more specialized. Agentic AI makes them action-oriented. MCP makes tool and data access more standardized. Agent Skills make capabilities reusable and operational. Together, these technologies can transform cybersecurity.

They can help analysts work faster, improve knowledge access, automate repetitive steps, and support better decisions. But they also create new risks. The more capable AI systems become, the more important governance, security, monitoring, and human oversight become. The future of AI in cybersecurity will not be defined only by better models. It will be defined by how responsibly we connect models to data, tools, workflows, and decisions.

The real question is not:

**How powerful is the AI model?**

The real question is:

**How safely, reliably, and responsibly can we use it in real cybersecurity operations?**

That is where the real work begins.

---

**How is your organization approaching LLMs, RAG, fine-tuning, agentic AI, MCP, and AI Skills?**

Are these technologies already part of your cybersecurity workflows — or still in the experimentation phase?

---

> Source: My own analysis and experience in my own AI lab, combined with documents such as:

[1]: https://owasp.org/www-project-top-10-for-large-language-model-applications/ "OWASP Top 10 for Large Language Model Applications"
[2]: https://modelcontextprotocol.io/docs/getting-started/intro "What is the Model Context Protocol (MCP)?"
[3]: https://www.anthropic.com/news/model-context-protocol "Introducing the Model Context Protocol"
[4]: https://agentskills.io/home "Agent Skills Overview - Agent Skills"
[5]: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview "Agent Skills - Claude API Docs"
[6]: https://www.nist.gov/itl/ai-risk-management-framework "AI Risk Management Framework | NIST"