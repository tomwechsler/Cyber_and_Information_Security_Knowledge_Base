# System Development Life Cycle: Why Security Must Be Built Into Every Phase

Digital systems rarely fail because one single control is missing.

They usually fail because security was treated as something separate from the business process, the architecture, the development process, the change process, the vendor relationship, or the operational lifecycle.

That is exactly why the **System Development Life Cycle (SDLC)** matters.

The SDLC is more than a project management model. It is a structured way to plan, design, acquire, build, test, deploy, operate, maintain, and retire systems in a controlled and repeatable manner. From an information security perspective, the real value of the SDLC is simple:

Security is not added at the end.

Security is integrated at every stage.

ISACA describes the SDLC as the phases used in the development or acquisition of a software system, including activities such as feasibility, requirements, design, programming, testing, installation, and post-implementation review. ([ISACA][1]) ISO/IEC/IEEE 12207 also takes a lifecycle view and applies to software systems, products, and services across conception, development, operations, support, retirement, acquisition, and supply. ([ISO][2])

## Why the SDLC Matters for Security

A lifecycle approach helps organizations avoid expensive and disruptive fixes later.

When security requirements are identified during initiation, the organization can make better architecture and budget decisions. When controls are designed during development or acquisition, they can be implemented more efficiently. When controls are tested before go-live, the organization reduces operational risk. When systems are monitored during operations, vulnerabilities can be addressed before they become incidents. And when systems are retired properly, data, identities, keys, interfaces, and dependencies do not remain forgotten in the environment.

In practical terms, a secure SDLC helps organizations:

- Reduce security defects before production.
- Align security requirements with business objectives.
- Support regulatory and contractual compliance.
- Improve documentation and auditability.
- Reduce rework and emergency remediation.
- Improve communication between business, IT, security, compliance, and vendors.
- Maintain secure systems throughout their full lifecycle.

The key point is this:

A secure system is not created only by secure coding.

A secure system is created by secure decisions across the entire lifecycle.

## Phase 1: Initiation — Define the Business Need and Security Direction

The SDLC starts before anyone writes code, configures infrastructure, or selects a vendor.

The initiation phase defines why the system is needed, what business objective it supports, which stakeholders are involved, what data will be processed, what risks may exist, and what security expectations must be considered from the beginning.

From a security perspective, this phase should answer several fundamental questions:

- What business process will this system support?
- What information will be processed, stored, or transmitted?
- Is personal data, financial data, intellectual property, healthcare data, or customer data involved?
- Who are the users and administrators?
- What regulatory, contractual, or internal policy requirements apply?
- What is the expected availability requirement?
- What could go wrong if the system is unavailable, manipulated, or misused?
- What is the organization’s risk appetite for this system?

Practical example:

A company wants to introduce a new customer portal.

At the initiation stage, the business may focus on customer experience and time-to-market. Security must add questions about authentication, data classification, encryption, logging, privacy, regulatory requirements, third-party integrations, and incident response.

If the portal processes customer contracts and payment-related information, the security requirements are very different from a simple public marketing website.

Key deliverables in this phase may include:

- Business case
- Initial risk assessment
- Data classification
- High-level security requirements
- Stakeholder map
- RACI matrix
- Regulatory and compliance overview
- Initial architecture assumptions
- Third-party dependency overview
- Security budget assumptions

A good initiation phase prevents one of the most common SDLC failures: discovering critical security requirements after design decisions have already been made.

## Phase 2: Development and Acquisition — Build, Buy, or Integrate Securely

The next phase focuses on turning requirements into a solution.

This may mean internal software development, purchasing a commercial product, integrating a SaaS platform, building a cloud-native service, adopting open-source components, or deploying an AI-assisted system.

Security has to be integrated regardless of whether the organization builds or buys.

For internally developed software, this phase includes:

- Secure architecture design
- Threat modeling
- Secure coding standards
- Code review
- Dependency management
- Secrets management
- Data protection design
- Authentication and authorization design
- Logging and monitoring design
- API security design
- Privacy-by-design principles
- Secure configuration baselines

For acquired systems, this phase includes:

- Vendor risk assessment
- Security questionnaires
- Contractual security requirements
- Data processing agreements
- Service level agreements
- Evidence such as SOC 2, ISO/IEC 27001, or penetration test summaries
- Software bill of materials where applicable
- Support and patching commitments
- Exit and data return clauses

NIST’s Secure Software Development Framework explains that many SDLC models do not explicitly address software security in detail, which is why secure software development practices need to be integrated into each SDLC implementation. ([NIST Computer Security Resource Center][3]) Microsoft’s Security Development Lifecycle similarly describes an approach for integrating security into DevOps processes. ([Microsoft][4])

Practical example:

An organization develops a new internal API for employee data.

A weak SDLC approach would build the API first and test security shortly before release.

A secure SDLC approach would define authorization rules during design, require secure coding practices during development, scan dependencies automatically, validate input handling, test API authorization, review logging, and ensure that sensitive fields are protected before deployment.

Another practical example:

A team wants to use an open-source library for authentication.

The secure SDLC does not simply ask whether the library works. It asks whether the library is maintained, whether known vulnerabilities exist, whether licenses are acceptable, whether updates are monitored, whether the dependency is pinned and verified, and whether the library introduces supply chain risk.

This is where software security and supply chain risk management meet.

## Phase 3: Implementation — Test, Validate, and Deploy With Control

Implementation is the point where the system moves from design and build into a real operating environment.

This phase is not only about technical deployment. It is about validating that the system is ready for production.

Security activities in this phase should include:

- Functional security testing
- Vulnerability scanning
- Static application security testing
- Dynamic application security testing
- Software composition analysis
- Infrastructure-as-code scanning
- Container image scanning
- Cloud configuration review
- Penetration testing where appropriate
- Access control validation
- Logging and alert validation
- Backup and recovery testing
- Change approval
- Deployment readiness review
- Go-live risk acceptance

Practical example:

A web application passes functional testing, but a dynamic security scan finds missing security headers, weak cookie settings, and an insecure file upload function.

A mature SDLC prevents go-live until the findings are reviewed, prioritized, remediated, or formally accepted by the appropriate risk owner.

Practical example:

A new cloud workload is ready for deployment.

Before release, the team validates that storage accounts are not public, managed identities follow least privilege, diagnostic logs are enabled, encryption is configured, secrets are stored in a key vault, and network exposure is limited.

This phase is also where documentation becomes important.

Security teams should document:

- What was tested
- What was found
- What was remediated
- What risks remain
- Who approved deployment
- What monitoring is in place
- What rollback plan exists
- What incident response process applies

Without documentation, security becomes difficult to prove.

And what cannot be proven is difficult to govern, audit, or improve.

## Phase 4: Operations and Maintenance — Keep the System Secure Over Time

A system that is secure on the day it goes live may not remain secure six months later.

- New vulnerabilities appear.
- Business requirements change.
- Users change roles.
- Vendors change products.
- Cloud services evolve.
- Attack techniques improve.
- Compliance expectations change.
- Data usage expands.
- AI tools and automation may introduce new dependencies.

This is why operations and maintenance are critical SDLC phases.

Security activities should include:

- Continuous monitoring
- Patch and vulnerability management
- Configuration management
- Access reviews
- Log review and alerting
- Incident response readiness
- Backup validation
- Certificate and key management
- Change management
- Security regression testing
- Vendor and dependency monitoring
- Periodic risk reassessment
- Control effectiveness reviews

Practical example:

A critical vulnerability is published for a component used by several internal applications.

A mature SDLC enables the organization to identify affected systems, prioritize remediation based on exposure and business criticality, test patches, deploy updates, and document the response.

A weak SDLC leaves teams guessing where the component is used.

Practical example:

A cloud system is modified to support a new business function.

Change management should ensure that the new feature does not accidentally expose data, bypass approval workflows, weaken access control, or disable logging.

This is where integrated change management becomes essential.

Security lifecycle activities must align with change management processes so that every major change is reviewed, documented, tested, and approved.

## Phase 5: Disposal — Retire Systems Securely

Disposal is one of the most underestimated SDLC phases.

Many organizations focus heavily on building and deploying systems, but they forget that old systems can remain dangerous long after they are no longer actively used.

- A retired system may still contain data.
- A legacy database may still have active accounts.
- A forgotten API may still be reachable.
- Old service accounts may still have privileges.
- Expired applications may still be connected to identity providers.
- Decommissioned servers may still contain secrets.
- Unused cloud resources may still generate cost and risk.

Secure disposal includes:

- Data retention review
- Data archival or secure deletion
- Account and access removal
- Key and certificate revocation
- DNS and firewall cleanup
- API deactivation
- Cloud resource removal
- Vendor contract closure
- Backup handling
- Evidence preservation where required
- CMDB and asset inventory updates
- Final risk and compliance documentation

Practical example:

A legacy HR application is replaced by a SaaS solution.

A secure disposal process ensures that employee data is migrated correctly, old data is archived according to retention requirements, administrator accounts are removed, database backups are handled appropriately, integrations are disabled, and the legacy server is decommissioned.

Disposal is not administrative cleanup.

It is a security control.

## SDLC From an ISACA Perspective

From an ISACA and information security management perspective, the SDLC is closely connected to governance, risk management, control design, assurance, and lifecycle accountability.

A security-oriented SDLC commonly includes:

- Initiation: Define and align security requirements with business objectives.
- Development and acquisition: Incorporate controls into system design, code, procurement, and architecture.
- Implementation: Test and validate controls before production use.
- Operations and maintenance: Monitor vulnerabilities, update controls, and manage change.
- Disposal: Securely archive, retire, destroy, or decommission systems and data.

This lifecycle view supports one of the most important security management principles:

Security must remain aligned with business value throughout the system’s life.

Not only at project start.

Not only at go-live.

Not only during audits.

Throughout the full lifecycle.

## How Other Frameworks and Standards Support the SDLC

The SDLC becomes stronger when it is connected to recognized frameworks and standards.

**ISO/IEC/IEEE 12207** provides a common framework for software life cycle processes and can be used to define, control, and improve lifecycle activities across organizations and projects. ([ISO][5])

**NIST SSDF** provides secure software development practices that can be integrated into different SDLC models, helping organizations reduce the risk of software vulnerabilities. ([NIST Computer Security Resource Center][3])

**Microsoft SDL** provides a practical secure development lifecycle approach that integrates security into DevOps and includes security requirements, tooling, and mandatory processes. ([Microsoft][4])

**OWASP SAMM** is an open framework that helps organizations create and implement a software security strategy and measure software assurance maturity. ([OWASP][6])

**NIST Cybersecurity Framework 2.0** organizes cybersecurity outcomes into Govern, Identify, Protect, Detect, Respond, and Recover, which can be mapped to SDLC activities and operational cybersecurity risk management. ([NIST Veröffentlichungen][7])

**ISO/IEC 27001** defines requirements for an information security management system and helps organizations establish, implement, maintain, and continually improve security management. ([ISO][8])

**COBIT** supports enterprise governance of information and technology and helps align technology governance with enterprise goals, processes, controls, and accountability. ([ISACA][9])

**CISA Secure by Design** emphasizes that software manufacturers should build products in a way that reduces the likelihood of successful compromise during the design phase and across the product lifecycle. ([CISA][10])

The point is not to choose only one framework.

The point is to combine them intelligently.

- ISACA can support governance and assurance.
- NIST can support secure engineering and risk management.
- ISO can support management systems and lifecycle structure.
- OWASP can support application security maturity and technical controls.
- Microsoft SDL can provide practical secure development patterns.
- COBIT can connect SDLC controls to enterprise governance.
- CISA Secure by Design can reinforce product security accountability.

Together, they help transform the SDLC from a project process into a security governance mechanism.

## SDLC in Agile, DevOps, and DevSecOps

A common misunderstanding is that the SDLC only applies to traditional waterfall projects.

That is not true.

The SDLC still matters in Agile, DevOps, and DevSecOps environments — but the controls need to be embedded differently.

In a waterfall model, security gates may occur at formal phase transitions.

In Agile, security needs to be part of epics, user stories, acceptance criteria, sprint planning, backlog refinement, definition of done, and release readiness.

In DevOps, security must be automated into CI/CD pipelines.

In DevSecOps, security becomes a shared responsibility across development, operations, security, architecture, compliance, and product ownership.

Practical examples:

- A user story includes security acceptance criteria.
- A pull request triggers static code analysis.
- A container image is scanned before deployment.
- A secrets scanner blocks committed credentials.
- Infrastructure-as-code templates are checked before cloud deployment.
- A dependency scanner opens tickets for vulnerable libraries.
- Threat modeling is performed for major architectural changes.
- Security tests are part of release pipelines.
- Evidence is stored automatically for audit purposes.

The modern SDLC is not about slowing delivery down.

It is about making secure delivery repeatable.

## The Role of AI and Modern Development Tools

Modern SDLC programs also need to consider AI-assisted development.

Developers increasingly use AI coding assistants, local LLMs, code generation tools, automated documentation, test generation, and AI-supported security analysis.

These tools can improve productivity, but they also introduce new control questions.

- Who may use AI-assisted coding tools?
- Can sensitive source code be submitted to external AI services?
- Are generated code suggestions reviewed?
- Are licenses and intellectual property risks considered?
- Are insecure code patterns detected?
- Are local LLMs patched and governed?
- Are AI-generated test cases validated?
- Are prompts and outputs logged appropriately?
- Is generated code included in normal peer review and security testing?

Practical example:

A developer uses an AI assistant to generate an authentication function.

The secure SDLC should ensure that the generated code is reviewed, tested, scanned, and validated like any other code. AI-generated output should never bypass secure coding standards, peer review, or security testing.

Practical example:

An organization uses a local LLM to summarize vulnerability scan results.

The secure SDLC should consider model provenance, access control, data classification, prompt logging, local infrastructure security, and whether sensitive vulnerability data is stored in prompts, embeddings, or logs.

AI does not replace the SDLC.

AI makes a disciplined SDLC even more important.

## Practical Security Gates Across the SDLC

A mature SDLC includes security gates.

These gates should not be bureaucratic obstacles. They should be decision points that help the organization control risk.

Examples:

- Before initiation approval: business objective, data classification, stakeholders, and initial risk must be defined.
- Before design approval: architecture, threat model, security requirements, privacy requirements, and third-party dependencies must be reviewed.
- Before development completion: code review, dependency review, secure coding checks, and unit security tests must be completed.
- Before go-live: vulnerability testing, access validation, logging validation, backup validation, and risk acceptance must be completed.
- During operations: vulnerabilities, changes, incidents, access, and control effectiveness must be monitored.
- Before disposal: data retention, access removal, decommissioning, and evidence requirements must be completed.

A good security gate answers three questions:

- What risk exists?
- Who owns the risk?
- What decision has been made?

## Practical Example: SDLC for a New Customer Portal

Let us make this concrete.

A company wants to build a customer portal.

During initiation, the organization defines business objectives, customer data types, authentication requirements, compliance obligations, availability needs, and initial risks.

During development and acquisition, the team designs secure authentication, role-based access, encryption, API security, logging, and session management. The team also reviews third-party components and cloud services.

During implementation, the organization performs vulnerability testing, validates access control, reviews logs, tests backup and recovery, and approves go-live.

During operations and maintenance, the system is patched, monitored, reviewed, and updated. User access is reviewed periodically. Incidents are handled through predefined response processes.

During disposal, data is archived or deleted according to retention requirements, accounts are removed, integrations are disabled, and infrastructure is decommissioned.

This is the SDLC in practice.

It is not just development.

It is governance, risk management, engineering, operations, compliance, and accountability working together.

## Practical Example: SDLC for a SaaS Procurement

Not every SDLC project involves custom code.

Suppose a company wants to introduce a SaaS platform for contract management.

During initiation, the business defines why the tool is needed and what data will be processed.

During acquisition, security reviews vendor certifications, encryption, identity integration, audit logs, data residency, incident notification clauses, subcontractors, backup processes, exit options, and support commitments.

During implementation, the team configures SSO, MFA, roles, logging, data import, approval workflows, and administrative access.

During operations, the organization monitors vendor changes, reviews access, checks audit logs, validates contractual obligations, and tracks service incidents.

During disposal, the company exports or deletes data, terminates access, confirms data deletion, and closes contractual obligations.

This is also SDLC.

Acquisition is part of the lifecycle.

## Practical Example: SDLC for Cloud Infrastructure

A cloud platform deployment also benefits from SDLC discipline.

During initiation, the team defines business purpose, data sensitivity, availability needs, regions, and compliance requirements.

During design, the architecture includes network segmentation, identity design, encryption, logging, backup, key management, and monitoring.

During implementation, infrastructure-as-code templates are scanned, cloud policies are applied, access roles are validated, and logging is enabled.

During operations, the environment is monitored for drift, vulnerabilities, suspicious activity, cost anomalies, and unauthorized changes.

During disposal, cloud resources are removed, secrets are revoked, logs are retained according to policy, and records are updated.

Cloud does not remove the SDLC.

Cloud makes lifecycle discipline even more important because systems can be created, changed, and forgotten very quickly.

## Metrics: How to Measure SDLC Effectiveness

An SDLC program should be measurable.

Useful metrics include:

- Percentage of projects with completed security requirements
- Percentage of systems with documented data classification
- Number of critical vulnerabilities found before production
- Number of critical vulnerabilities found after production
- Mean time to remediate vulnerabilities
- Percentage of systems with completed threat models
- Percentage of releases passing security gates
- Number of emergency fixes caused by missed security requirements
- Percentage of third-party systems with completed risk assessments
- Percentage of systems with documented disposal plans
- Number of overdue access reviews
- Number of unresolved high-risk exceptions

The purpose of metrics is not reporting for reporting’s sake.

The purpose is to improve decision-making.

Good SDLC metrics help leaders understand whether security is embedded early enough, whether controls are effective, and whether risk is being reduced over time.

## Common SDLC Mistakes

Many organizations struggle with the same issues.

- Security is involved too late.
- Requirements focus only on functionality.
- Threat modeling is skipped.
- Third-party risk is underestimated.
- Developers lack secure coding guidance.
- Testing focuses only on functionality.
- Logging is added after incidents occur.
- Operational ownership is unclear.
- Change management is weak.
- Legacy systems are not retired properly.
- Security exceptions are accepted but not reviewed later.
- AI-generated code is trusted too quickly.
- Cloud resources are deployed without lifecycle ownership.

The solution is not more paperwork.

The solution is clearer ownership, better integration, stronger automation, and consistent governance.

## Final Thoughts

The System Development Life Cycle is often described as a technical process.

In reality, it is a business risk management process.

- Every system supports a business objective.
- Every system processes information.
- Every system introduces dependencies.
- Every system creates risk.
- Every system requires ownership.
- Every system eventually changes.
- Every system eventually reaches end of life.

A mature SDLC ensures that security is considered from the first idea to final retirement.

It helps organizations move from reactive security to proactive security.

It connects business objectives, architecture, development, acquisition, testing, operations, compliance, and disposal.

And most importantly:

It prevents security from becoming a late-stage problem.

Because the most effective security control is often not the one added after an incident.

It is the one designed into the lifecycle from the beginning.

---

Sources: My own PowerPoint slides, analysis and experience in my own AI lab, combined with standards and documents such as the:

[1]: https://www.isaca.org/resources/glossary "ISACA® Interactive Glossary"
[2]: https://www.iso.org/standard/90219.html "ISO/IEC/IEEE 12207:2026 - Software life cycle processes"
[3]: https://csrc.nist.gov/pubs/sp/800/218/final "Secure Software Development Framework (SSDF) Version 1.1"
[4]: https://www.microsoft.com/en-us/securityengineering/sdl "Microsoft Security Development Lifecycle (SDL)"
[5]: https://www.iso.org/standard/90219.html "ISO/IEC/IEEE 12207:2026 - Systems and software ..."
[6]: https://owasp.org/www-project-samm/ "OWASP SAMM"
[7]: https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf "The NIST Cybersecurity Framework (CSF) 2.0"
[8]: https://www.iso.org/standard/27001 "ISO/IEC 27001:2022 - Information security management ..."
[9]: https://www.isaca.org/resources/cobit "COBIT®| Control Objectives for Information Technologies®"
[10]: https://www.cisa.gov/securebydesign "Secure by Design"