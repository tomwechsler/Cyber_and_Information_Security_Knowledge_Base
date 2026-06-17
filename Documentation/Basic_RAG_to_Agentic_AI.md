# From Basic RAG to Agentic AI: Why MCP and Security Matter

Artificial Intelligence is moving fast.

Many organizations started their AI journey with simple chatbots, then moved to Retrieval-Augmented Generation, and are now exploring agentic systems that can plan, reason, retrieve, call tools, interact with APIs, and support real business workflows.

This evolution is powerful.

But it also changes the security model.

A basic Large Language Model answers questions based on its training data and the current prompt. A RAG system extends the model with external knowledge. Agentic RAG adds dynamic retrieval and task planning. Agentic AI goes even further by allowing the system to use tools, make decisions, and execute multi-step workflows.

And once AI systems can access data, tools, identities, APIs, databases, email, tickets, cloud services, or security platforms, they are no longer just “AI applications”.

They become part of the enterprise attack surface.

This is where the Model Context Protocol, or MCP, becomes highly relevant. MCP is an open protocol designed to connect LLM applications with external data sources and tools in a standardized way. ([Model Context Protocol][1])

The question is no longer only:

Can we build intelligent AI systems?

The real question is:

Can we build intelligent AI systems that are secure, controlled, observable, and aligned with business risk?

## 1. Starting Point: The LLM Alone

A Large Language Model can generate text, summarize information, explain concepts, create code, classify content, and support analysis.

But by itself, an LLM is limited.

- It does not automatically know your internal documentation.
- It does not know your latest policies.
- It does not know your current incidents.
- It does not know your latest vulnerability scan results.
- It does not know your company-specific architecture.
- It does not know what happened in your SIEM ten minutes ago.

An LLM alone is useful for general reasoning and language tasks, but it lacks trusted organizational context.

In cybersecurity, this matters.

A security analyst asking, “What is our response process for a suspected credential theft incident?” does not need a generic internet answer. The analyst needs the organization’s actual incident response playbook, escalation matrix, evidence requirements, legal notification process, and containment steps.

This is the gap that Retrieval-Augmented Generation tries to close.

## 2. Basic RAG: Bringing Knowledge to the Model

Retrieval-Augmented Generation, or RAG, connects an LLM to external knowledge.

A basic RAG architecture usually contains three main components:

The user asks a question.
The RAG application searches a knowledge base or vector database.
The LLM receives the user prompt, system instructions, and retrieved document chunks to generate a more grounded answer.

In practice, this means that internal documents can be indexed and searched semantically. Instead of relying only on the model’s training data, the system retrieves relevant content from approved sources.

A typical basic RAG workflow looks like this:

1. Documents are collected.
2. Documents are split into chunks.
3. Chunks are transformed into embeddings.
4. Embeddings are stored in a vector database.
5. A user submits a query.
6. The system performs semantic search.
7. Relevant chunks are added to the prompt.
8. The LLM generates an answer based on the retrieved context.

For cybersecurity, Basic RAG can be very useful.

Practical examples include:

- A security policy assistant that answers questions based on internal policies.
- A compliance assistant that retrieves evidence requirements for ISO/IEC 27001 controls.
- An incident response assistant that explains internal escalation procedures.
- A vulnerability management assistant that summarizes remediation guidance from internal standards.
- A SOC knowledge assistant that retrieves detection engineering notes, runbooks, and playbooks.

Basic RAG is especially helpful when accuracy depends on organization-specific knowledge.

However, Basic RAG also has limitations.

It usually follows a predefined path. It retrieves context from one or more sources and passes that context to the model. The system may not dynamically decide which tools to use, whether to search multiple systems, whether to ask a follow-up question, or whether to validate information through several steps.

In short:

Basic RAG improves knowledge access.

But it does not automatically create intelligent workflow execution.

## 3. From Basic RAG to AI Workflows

Before discussing agents, it is important to understand AI workflows.

An AI workflow uses one or more LLM calls inside a predefined process.

Examples include prompt chaining, routing, parallelization, evaluator-optimizer patterns, and orchestrator-worker patterns.

In a prompt chaining workflow, one LLM call produces an output that becomes the input for the next step.

For example:

Step 1: Summarize a suspicious email.
Step 2: Extract indicators of compromise.
Step 3: Classify the phishing risk.
Step 4: Generate a recommended response.

In a routing workflow, the system decides which specialized path to use.

For example:

- If the question is about identity, route it to IAM documentation.
- If the question is about cloud security, route it to Azure or AWS controls.
- If the question is about incident response, route it to the IR playbook.
- If the question is about vulnerabilities, route it to CVE and remediation sources.

In an evaluator-optimizer workflow, one model generates an answer and another step checks or improves it.

For example:

One component drafts an incident summary.
Another evaluates whether the summary includes timeline, scope, impact, containment, eradication, recovery, and lessons learned.

Workflows are powerful because they add structure.

But they are still mostly predefined.

The LLM may be embedded in a workflow, but the workflow itself controls the path.

Agentic AI changes this relationship.

## 4. Agentic AI: When the Model Starts to Direct the Process

Agentic AI describes AI systems that can pursue goals through planning, reasoning, tool use, memory, and multi-step execution.

Instead of simply answering a prompt, an AI agent may decide what steps are needed to complete a task.

- It may break down a complex request.
- It may choose tools.
- It may retrieve data.
- It may call APIs.
- It may evaluate intermediate results.
- It may adjust the plan.
- It may ask for clarification.
- It may produce a final response after several steps.

This is fundamentally different from a simple chatbot.

A chatbot responds.

An agent acts within a controlled environment.

In cybersecurity, this could mean:

- An agent receives a suspicious domain.
- It checks threat intelligence.
- It searches internal DNS logs.
- It queries SIEM events.
- It checks endpoint telemetry.
- It summarizes findings.
- It recommends containment actions.
- It creates a ticket.
- It asks for human approval before blocking the domain.

This is powerful.

But it also introduces risk.

An AI system that only generates text has limited direct impact.

An AI system that can access tools, query systems, trigger workflows, modify records, send emails, or execute commands can create operational, security, privacy, and compliance consequences.

This is why Agentic AI must be designed with security from the beginning.

## 5. Agentic RAG: Dynamic Retrieval and Multi-Step Reasoning

Agentic RAG combines retrieval with agentic behavior.

A Basic RAG system usually performs retrieval in a relatively fixed way. It searches a vector database, retrieves relevant chunks, and passes them to the model.

Agentic RAG is more dynamic.

- It can decide where to search.
- It can perform multiple retrieval steps.
- It can use different data sources.
- It can combine vector search with web search, databases, APIs, or internal tools.
- It can evaluate whether the retrieved context is sufficient.
- It can refine the query.
- It can compare results from multiple sources.
- It can reason across several steps.

For example, a Basic RAG system might answer:

“What does our incident response policy say about ransomware?”

An Agentic RAG system could handle a more complex task:

“Review the latest ransomware alert, compare it with our internal incident response playbook, check whether we have affected systems in our asset inventory, and draft a recommended containment plan.”

This task requires more than retrieval.

It requires planning, routing, tool use, context evaluation, and controlled action.

Agentic RAG can be especially useful in cybersecurity because security work is rarely one-step work.

- Investigations require context.
- Context comes from different systems.
- Evidence must be validated.
- Actions must be prioritized.
- Decisions often require human approval.

Agentic RAG can support this process — but it must not bypass governance.

## 6. Types of AI Agents in Practice

Different agent patterns can be used depending on the task.

A routing agent directs a query to the most relevant source or workflow.

Example: A user asks about privileged access. The routing agent sends the query to IAM policies, PAM procedures, and access review documentation.

A query planning agent breaks a complex question into sub-questions.

Example: “Assess the security posture of this web application” becomes: check architecture, authentication, exposed services, vulnerability scan results, logging, data sensitivity, and compliance requirements.

A ReAct agent combines reasoning and action.

Example: The agent thinks through the investigation, calls a threat intelligence tool, reviews results, performs another search, and then summarizes the finding.

A dynamic planning agent separates high-level planning from execution.

Example: For a suspected cloud incident, the agent creates an investigation plan, queries logs, checks identity events, reviews resource changes, and recommends containment.

A retrieval agent specializes in finding relevant knowledge.

Example: One retrieval agent searches internal policies, another searches vectorized incident reports, another queries vulnerability data, and another checks web-based threat intelligence.

In a mature architecture, agents should not all have the same privileges.

A read-only knowledge retrieval agent is not the same as an agent that can disable accounts or trigger firewall changes.

Security architecture must reflect that difference.

## 7. MCP: A Standardized Way to Connect AI to Tools

As AI systems become more capable, they need standardized ways to connect to external systems.

This is where the Model Context Protocol becomes important.

MCP provides a standardized approach for connecting LLM applications to external tools and data sources. Instead of building many custom integrations, MCP can act as a consistent interface between the AI application and external capabilities. ([Model Context Protocol][1])

In simple terms, MCP can help connect an AI application to systems such as:

- Vector databases
- File repositories
- Web search
- Ticketing systems
- Email systems
- Security tools
- Cloud APIs
- Vulnerability databases
- Internal knowledge bases
- Business applications
- Developer tools
- Monitoring platforms

For a cybersecurity use case, an MCP-enabled AI assistant could connect to:

- A CVE database
- A SIEM search interface
- A ticketing system
- A vulnerability scanner
- A threat intelligence source
- An internal policy repository
- A security knowledge base
- A cloud inventory tool
- A detection engineering repository

This creates a more scalable integration model.

However, standardized connectivity also means standardized risk.

If an AI application can reach many tools through MCP, then authentication, authorization, logging, approval workflows, and least privilege become essential.

The MCP documentation specifically highlights secure authorization patterns, including OAuth 2.1, for protecting sensitive resources and operations. ([Model Context Protocol][2])

## 8. Local LLMs: More Control, More Responsibility

Many organizations are exploring local LLMs.

A local LLM can run on internal infrastructure, a workstation, a private server, or an isolated lab environment. Tools such as local model runtimes, local web interfaces, vector databases, and internal document stores make it possible to build private AI environments.

This can be very attractive for cybersecurity.

Local LLMs can support:

- Security awareness content generation
- Policy analysis
- Log summarization
- Incident report drafting
- Threat modeling exercises
- Lab environments
- RAG over internal documentation
- Cybersecurity training
- Detection engineering assistance
- Secure experimentation

Local deployment can reduce dependency on external AI providers and may help protect sensitive data.

But local does not automatically mean secure.

A local AI environment still has a supply chain.

It includes the model, runtime, Python packages, container images, plugins, vector databases, UI components, scripts, connectors, operating system, GPU drivers, and datasets.

Security questions are essential:

- Where was the model downloaded from?
- Can the model file be verified?
- Are dependencies patched?
- Are plugins reviewed?
- Is the web interface protected?
- Is authentication enabled?
- Is the vector database encrypted?
- Is sensitive data stored in embeddings?
- Are prompts and outputs logged securely?
- Can the local LLM access the internet?
- Can it call tools or execute commands?
- Who is allowed to use it?

Local LLMs provide more control.

But more control also means more operational responsibility.

## 9. Practical Example: Basic RAG for Internal Security Policies

Imagine an organization wants to help employees understand internal security policies.

A Basic RAG system can index documents such as:

- Acceptable Use Policy
- Password Policy
- Remote Work Policy
- Incident Reporting Procedure
- Data Classification Policy
- Cloud Security Standard
- Phishing Reporting Guide

An employee can ask:

“Can I upload customer data to an external AI tool?”

The RAG system searches approved internal policies and returns an answer based on the organization’s own rules.

This is a strong use case for Basic RAG because the task is knowledge retrieval and explanation.

- The system does not need to execute actions.
- It does not need privileged access.
- It does not need to call production systems.

The risk is manageable if the knowledge base is curated, access-controlled, logged, and regularly updated.

## 10. Practical Example: Agentic RAG for Vulnerability Management

Now consider vulnerability management.

A security analyst asks:

“Which critical vulnerabilities affect our internet-facing systems, and what should we prioritize this week?”

A Basic RAG system may retrieve vulnerability management policies.

An Agentic RAG system could do more:

- Search the asset inventory.
- Identify internet-facing systems.
- Query vulnerability scan results.
- Check exploitability information.
- Compare findings with business criticality.
- Look up remediation guidance.
- Generate a prioritized action list.
- Create draft tickets for approval.

This is far more useful.

But it is also riskier.

The system now touches operational data. It may access sensitive infrastructure information. It may create tickets. It may influence prioritization.

Therefore, the design should include:

- Read-only access by default
- Clear source attribution
- Human approval before ticket creation
- Logging of all tool calls
- Role-based access control
- Separation between recommendation and execution
- Validation of vulnerability data
- Protection against prompt injection in retrieved content

Agentic RAG must be treated as a security-relevant application.

## 11. Practical Example: MCP-Based SOC Assistant

A SOC assistant using MCP could connect to several tools:

- A SIEM for log searches
- A threat intelligence platform
- A ticketing system
- A vulnerability database
- An internal incident response knowledge base
- A cloud inventory source
- A case management system

An analyst asks:

“Investigate whether this IP address appears in recent suspicious activity.”

The assistant could:

- Search SIEM logs.
- Check threat intelligence.
- Look for related alerts.
- Identify affected hosts.
- Summarize the timeline.
- Recommend severity.
- Draft an incident ticket.

This can save time and improve consistency.

But the SOC assistant must not become an uncontrolled super-user.

Security requirements should include:

- Named user context
- Strong authentication
- Least privilege
- Tool-specific authorization
- Audit logs
- Approval gates for actions
- Rate limits
- Input validation
- Output validation
- Data classification controls
- Monitoring of agent behavior
- Incident response procedures for AI misuse

In a SOC, speed matters.

But control matters just as much.

## 12. Security Risks in RAG, Agentic AI and MCP

The security risks increase as AI systems become more connected and autonomous.

For Basic RAG, common risks include:

- Poor document quality
- Outdated knowledge
- Sensitive data in the knowledge base
- Unauthorized access to indexed content
- Prompt injection through retrieved documents
- Incorrect source selection
- Hallucinated answers despite retrieval
- Embedding leakage
- Weak vector database security

For Agentic RAG, additional risks include:

- Incorrect tool selection
- Overly broad retrieval
- Unvalidated multi-step reasoning
- Misleading intermediate results
- Excessive autonomy
- Unclear accountability
- Lack of human approval
- Poor observability
- Cascading errors across steps

For Agentic AI, the risks expand further:

- Tool misuse
- Privilege escalation
- Sensitive data exposure
- Unauthorized actions
- Identity spoofing
- Memory poisoning
- Goal manipulation
- Unsafe code execution
- Uncontrolled API access
- Lack of auditability
- Unexpected behavior in complex workflows

For MCP-enabled environments, key risks include:

- Unmonitored access
- Insufficient authorization
- Weak token handling
- Lack of approval workflows
- Limited audit trails
- Overprivileged MCP servers
- Insecure tool exposure
- Credential leakage
- Unsafe transport security
- Insufficient input validation

The OWASP Top 10 for LLM Applications highlights several risks that are directly relevant here, including prompt injection, sensitive information disclosure, supply chain vulnerabilities, data and model poisoning, improper output handling, excessive agency, system prompt leakage, vector and embedding weaknesses, misinformation, and unbounded consumption. ([OWASP Gen AI Security Project][3])

MITRE ATLAS is also highly useful because it provides a knowledge base of adversary tactics and techniques against AI-enabled systems based on real-world observations and demonstrations. ([atlas.mitre.org][4])

## 13. Security Architecture Principles

A secure architecture for RAG, Agentic RAG, Agentic AI, and MCP should follow strong security principles.

The first principle is least privilege.

An AI assistant should only access the data and tools needed for its task. A policy assistant does not need access to production systems. A vulnerability assistant may need read-only scanner data, but not administrative cloud permissions.

The second principle is separation of duties.

Recommendation and execution should be separated. An agent may recommend disabling a user account, but a human or a separate approved workflow should authorize the action.

The third principle is human-in-the-loop for high-impact actions.

Blocking traffic, deleting data, disabling accounts, changing firewall rules, modifying IAM roles, or sending external communications should require approval.

The fourth principle is strong authentication and authorization.

MCP servers, tools, users, and agents should be authenticated. Authorization should be explicit, scoped, and continuously reviewed.

The fifth principle is observability.

Every tool call, retrieval step, decision, prompt, response, and action should be logged in a way that supports troubleshooting, compliance, and incident response.

The sixth principle is secure data handling.

Sensitive data should be classified, minimized, encrypted, masked where appropriate, and protected from unauthorized retrieval or leakage.

The seventh principle is secure-by-design integration.

AI systems should not be connected directly to critical tools without guardrails, validation, monitoring, and emergency shutdown options.

## 14. Frameworks and Standards That Help

Several frameworks and standards can support secure implementation.

NIST AI RMF is highly relevant for governing AI risk. Its core functions are Govern, Map, Measure, and Manage, providing a structured approach for understanding and managing AI risks across the lifecycle. ([NIST][5])

NIST Cybersecurity Framework 2.0 can help integrate AI and agentic systems into broader cybersecurity governance, risk management, protection, detection, response, and recovery activities.

ISO/IEC 27001 and ISO/IEC 27002 support information security governance, access control, supplier relationships, logging, incident management, and secure operations.

ISO/IEC 42001 provides a management system approach for AI governance and is especially relevant for organizations building or operating AI systems.

ISO/IEC 23894 provides guidance for AI risk management.

OWASP Top 10 for LLM Applications provides practical risk categories for LLM-based systems. ([OWASP Gen AI Security Project][3])

MITRE ATLAS helps security teams understand AI-specific adversarial tactics and techniques. ([atlas.mitre.org][4])

For software and AI supply chain security, organizations should also consider secure development practices, SBOMs, dependency scanning, signed artifacts, trusted repositories, and vulnerability management.

For MCP specifically, secure authorization, token handling, TLS, RBAC, audit logging, and explicit tool permissions are essential.

## 15. Practical Security Checklist

A practical checklist for secure implementation should include the following areas.

For Basic RAG:

- Use approved data sources.
- Classify and protect documents.
- Control access to indexed content.
- Keep the knowledge base updated.
- Monitor retrieval quality.
- Protect the vector database.
- Prevent sensitive data leakage.
- Validate outputs.
- Cite or reference sources where possible.

For Agentic RAG:

- Define allowed tools.
- Limit autonomy by task type.
- Use human approval for high-impact actions.
- Log every tool call.
- Validate intermediate results.
- Apply rate limits.
- Use role-based access.
- Prevent prompt injection through retrieved content.
- Monitor abnormal agent behavior.

For MCP:

- Use strong authentication.
- Use OAuth 2.1 or appropriate enterprise identity patterns where applicable.
- Use TLS for transport security.
- Store credentials securely.
- Use short-lived tokens.
- Apply RBAC and ACLs.
- Separate MCP servers by sensitivity.
- Limit tool permissions.
- Log requests and responses.
- Monitor for misuse.
- Disable unused tools.
- Review integrations regularly.

For local LLMs:

- Use trusted model sources.
- Verify model files where possible.
- Scan containers and dependencies.
- Restrict network access.
- Protect local web interfaces.
- Avoid indexing sensitive data unnecessarily.
- Secure vector databases.
- Review plugins before use.
- Document model versions.
- Monitor prompts, outputs, and tool calls.

## 16. What Many Organizations Miss

Many organizations underestimate the transition from AI assistant to AI actor.

A chatbot that answers questions is one thing.

An agent that retrieves data, calls tools, accesses systems, updates tickets, sends messages, or executes scripts is something else.

The risk increases when AI systems gain:

- Memory
- Tool access
- API access
- Identity context
- External connectivity
- Business process integration
- Autonomous planning
- Write permissions
- Multi-agent communication
- Access to sensitive data

Another common mistake is treating AI security as only a model problem.

In reality, most enterprise AI risk is system risk.

The model is only one component.

The full system includes data, prompts, retrieval pipelines, vector databases, APIs, plugins, identities, permissions, tools, logs, users, workflows, infrastructure, and governance.

Secure AI requires securing the entire ecosystem.

## 17. A Practical Implementation Roadmap

A pragmatic roadmap could look like this.

Start with Basic RAG.

Use low-risk internal documentation such as policies, procedures, FAQs, and training material. Keep the system read-only. Validate retrieval quality. Protect access. Monitor usage.

Then introduce controlled workflows.

Add routing, prompt chaining, evaluation, and structured outputs. Keep actions limited and predictable.

Next, move to Agentic RAG.

Allow the system to plan retrieval steps, query multiple sources, and support more complex tasks. Maintain strong logging and human oversight.

Then integrate tools through MCP or similar controlled interfaces.

Start with read-only tools. Use strong authentication. Apply least privilege. Separate tool scopes. Review every integration.

Only then consider higher-impact agentic actions.

For example, creating tickets may be allowed before disabling accounts. Drafting a firewall change may be allowed before applying it. Recommending containment may be allowed before executing containment.

Finally, operationalize governance.

Define owners, policies, risk assessments, testing processes, monitoring, incident response, and continuous improvement.

AI should not be deployed as a side experiment forever.

Once it supports real workflows, it must become part of enterprise governance.

## Final Thoughts

The evolution from Basic RAG to Agentic RAG, Agentic AI, and MCP-enabled tool integration is one of the most important developments in enterprise AI.

Basic RAG gives the model knowledge.

Agentic RAG gives it dynamic retrieval and reasoning.

Agentic AI gives it planning and action.

MCP gives it a standardized way to connect with tools and data sources.

Together, these capabilities can transform cybersecurity operations, compliance, incident response, vulnerability management, awareness training, and risk management.

But they also change the security equation.

The more capable the AI system becomes, the more important governance, identity, access control, monitoring, human approval, secure architecture, and risk management become.

The future of AI in cybersecurity is not just about smarter models.

It is about secure systems.

Because once AI can access tools, data, and workflows, the key question is no longer:

What can the AI answer?

The key question becomes:

What can the AI do — and how do we control it?

That is where secure AI architecture begins.

---

> Source: My own analysis and experience in my own AI lab, combined with documents and standards such as the:

[1]: https://modelcontextprotocol.io/specification/2025-11-25 "Specification"
[2]: https://modelcontextprotocol.io/docs/tutorials/security/authorization "Understanding Authorization in MCP"
[3]: https://genai.owasp.org/llm-top-10/ "LLMRisks Archive - OWASP Gen AI Security Project"
[4]: https://atlas.mitre.org/ "MITRE ATLAS™"
[5]: https://www.nist.gov/itl/ai-risk-management-framework "AI Risk Management Framework | NIST"