# Can It, and Should It? Securing the AI Lifecycle from Use Case to Human Oversight!

**Author:** Tom Wechsler

> *Can an AI system perform the task, and should it be trusted with that level of authority? A practical guide to securing every stage of the AI lifecycle.*

Every AI project has to answer two questions. Most teams only ask the first one.

The first question is technical: can the AI perform this task? Can a model reliably tell a phishing email from a legitimate invoice, summarize an incident, or flag a fraudulent payment? Proofs of concept, benchmarks and vendor demos are built to answer it, and they usually answer yes.

The second question is about trust: should the AI be trusted with this level of authority? Should it only label a message, or quarantine it, or delete it from every mailbox in the company without anyone looking? That question is not answered by accuracy alone. It is answered by how the system was designed, built, tested, deployed, monitored and governed over its whole life.

This article walks through that whole life, the AI lifecycle, stage by stage, and shows where security belongs in each one. To keep it practical, I follow one realistic project throughout: Veltrax Logistics, a fictional mid-sized logistics company with around 4,000 employees, decides to build a machine learning model that detects phishing emails. Along the way I connect each stage to the frameworks security teams already use.

## 1. The AI lifecycle at a glance

The AI lifecycle, often called the model development lifecycle, is not a straight line from idea to production. It is a loop, because AI systems evolve: feedback and monitoring continuously drive improvement. A practical version has nine stages:

- **Business use case:** define the problem, objectives, success criteria and constraints.
- **Data collection:** collect data from trusted sources with integrity, privacy and authenticity.
- **Data preparation:** clean, label, transform and prepare data for training and testing.
- **Model development:** select the architecture, train the model and manage dependencies securely.
- **Model evaluation:** evaluate performance, bias, robustness and security before deployment.
- **Deployment:** move the model to production securely with proper access controls.
- **Validation:** validate in real-world conditions using shadow or canary deployments.
- **Monitoring:** continuously monitor performance, drift, security and system behavior.
- **Feedback and iteration:** use insights and feedback to refine and improve the system, which leads back to the use case.

### Security is a continuous responsibility

The most important lesson from this loop is that security cannot be a gate at the end. It has to protect data, models and systems at every stage, through four recurring themes: data security, model protection, access control, and monitoring and oversight.

Five principles follow from that:

- Security starts before development. The riskiest decisions, such as how much authority the model gets and which data it may see, are made in the first stage.
- Early mistakes create lasting risk. A poisoned data source or a bad labelling process is baked into every model trained afterwards.
- Every phase introduces its own attack surface. Data pipelines, training environments, model registries, APIs and feedback channels all need protection.
- Monitoring drives improvement. Without telemetry you cannot tell degradation from attack.
- Security is continuous. A model that was safe at launch can become unsafe without a single line of code changing.

None of this replaces the classic security disciplines. People need awareness and training, processes need policies and procedures, technology needs controls and monitoring, and governance needs risk management, compliance and accountability. AI adds new assets to protect, not a new philosophy.

## 2. Business use case: where security really begins

At Veltrax, the security team receives several hundred user-reported emails per week, and analysts spend hours triaging messages that turn out to be newsletters. Meanwhile, invoice fraud attempts targeting the finance team are getting more convincing. The business case writes itself: reduce analyst workload, improve phishing detection, accelerate incident response, reduce operational costs, and improve the experience for employees who report suspicious mail.

A good use case document goes further than goals. It defines:

- **Objectives:** for example, cut manual triage time by half and catch credential phishing that the existing gateway misses.
- **Success criteria:** measurable targets such as recall on known phishing above an agreed threshold, with a false positive rate low enough that finance and sales do not lose legitimate customer emails.
- **Constraints:** data protection rules for email content, works council agreements on employee monitoring, budget, and the requirement that the existing mail gateway stays in place as a backstop.

This is also where the two questions from the introduction get their first answer. Veltrax defines the model's authority in explicit tiers:

- **Advise:** add a warning banner and a risk score to the email. Fully automatic.
- **Contain:** move a high-confidence phishing email to quarantine. Automatic, but reversible by the user or the SOC.
- **Act across the organization:** remove a message from every mailbox or block a sender domain. Only after analyst approval.

That single definition of authority will shape every later stage: what data is needed, how strict evaluation must be, which controls deployment requires and where humans stay in the loop. A threat model at this stage, even a simple one, pays off. Ask how an attacker would want this model to fail, and who would benefit from making it miss a specific kind of email.

## 3. Data collection: trustworthiness and authenticity

Veltrax has three natural data sources: two years of emails reported by employees, messages already quarantined by the mail gateway, and a commercial threat intelligence feed with phishing samples. Each must pass two tests.

### Is the data trustworthy?

- **Representative data:** the training data must reflect the users, systems and threats the model will actually see. A data set dominated by consumer spam says little about invoice fraud against a logistics finance team.
- **Real-world conditions:** data should mirror today's environment, not an idealized or outdated one. Phishing from three years ago rarely used QR codes or links to legitimate file-sharing services; today's does.
- **Edge cases included:** rare and unusual messages, such as German and French lures, emails from compromised supplier accounts, and calendar invitations, make the model more resilient.
- **Reliable sources:** data should come from trusted, verified and well-maintained sources.
- **Minimize blind spots:** diverse data reduces the coverage gaps that attackers or unforeseen conditions could exploit.

### Is the data authentic?

Authenticity is the security side of the same coin. The goals are to prevent data poisoning, verify data origin, detect tampering, validate source attribution and maintain data governance.

Here is the uncomfortable detail in the Veltrax design: the user-reported mailbox is open to anyone who can send an email to an employee. An attacker who knows that reported messages become training data could flood it with carefully crafted samples. The mitigation is not to drop the source, but to treat it as untrusted input: only messages confirmed by an analyst become labels, every sample keeps a record of where it came from, and the ingestion pipeline stores a hash so later tampering is detectable. The external feed gets a contract clause on data quality and a review of how the vendor labels its samples.

## 4. Data preparation: where quality and security meet

Data preparation turns raw material into training material. It has five parts, and each one has a security angle.

- **Clean and normalize data.** Remove duplicates, unify encodings and time zones, and strip tracking pixels or attachments that are not needed. At Veltrax, one campaign hit 900 employees, so the same email exists 900 times. Without deduplication, the model overlearns that campaign.
- **Label training examples.** Every email gets a verdict, and labels are the most attractive target for manipulation. Veltrax requires two independent analysts for any label on a high-risk sample, and logs who labelled what.
- **Engineer features.** Features such as sender age, reply-to mismatches, link domains, authentication results (SPF, DKIM, DMARC) and urgency cues make the model useful. They also define what an attacker must imitate to evade it, so feature documentation is sensitive.
- **Create train, test and validation splits.** The classic pitfall is leakage. If copies of the same campaign land in both training and test data, the test score is inflated and meaningless. Veltrax splits by campaign and by time: the model trains on older months and is tested on the most recent ones, which mimics how it will be used in reality.
- **Protect preparation systems.** The notebooks, scripts, storage buckets and labelling tools used here hold sensitive email content and directly shape the model. They need the same access control, logging and change management as any production system. A single overly permissive storage bucket can undo every other control in this article.

## 5. Model development and selection

This is the stage most people picture when they think of AI, and it has five responsibilities.

- **Select the model architecture.** Veltrax compares two options: a gradient-boosted model on engineered email features, and a fine-tuned Transformer that reads the full email text. The Transformer understands language better; the gradient-boosted model is faster, cheaper and far easier to explain to an analyst. Many teams end up combining them. The choice is a security decision too, because explainability affects how quickly an analyst can trust or challenge a verdict.
- **Train using labelled phishing data.** Training uses only the verified, versioned data set from the previous stage, identified by its hash, so the exact training data of every model version can be reproduced later.
- **Secure the training environment.** Training infrastructure holds the most sensitive data in the project and produces the most valuable artifact. It belongs in an isolated environment with restricted network egress, dedicated service identities, no shared credentials and full audit logging.
- **Manage dependencies and frameworks.** An AI project pulls in machine learning libraries, tokenizers and often a pretrained base model from a public hub. That is a software supply chain like any other, with one extra trap: some common model file formats, such as Python pickle files, can execute code when they are loaded. Security researchers have repeatedly found malicious models uploaded to public model hubs. Practical controls are pinned versions, dependency scanning, an internal mirror for approved models, and safer serialization formats such as safetensors.
- **Document training decisions.** Which data version, which hyperparameters, which base model, which known limitations, and who approved it. A short model card per version is enough. When an auditor or an incident responder asks why the model behaves the way it does, this documentation is the only reliable answer.

## 6. Model evaluation: does it work, and how does it fail?

Evaluation answers the first of our two questions with evidence. It covers five activities.

- **Test with unseen emails.** Veltrax holds back the most recent two months: 20,000 emails, of which 400 are confirmed phishing. The model never saw any of them during training.
- **Measure precision and recall.** The model catches 376 of the 400 phishing emails, a recall of 94 percent. It also flags 98 legitimate emails, a false positive rate of 0.5 percent. Precision, the share of flagged emails that really are phishing, is therefore about 79 percent. Note how different those numbers feel: "94 percent detection" sounds excellent, while "one in five alerts is wrong" sounds like work. Both are true, and decision makers need to see both.
- **Analyze false positives.** Most of the 98 false alarms are automated booking confirmations from a legitimate freight platform that uses urgent language and link shorteners. That is fixable with better features and an allowlisting process that has its own approval and review.
- **Analyze false negatives.** Most of the 24 misses are QR code phishing, where the malicious link sits inside an image the model cannot read, and two are replies from a genuinely compromised supplier mailbox. Those are not tuning issues. They are blind spots that need another control, such as image analysis or out-of-band verification for payment changes.
- **Determine deployment readiness.** The decision is tied back to the authority tiers. Veltrax approves the advisory banner for all emails and automatic quarantine only above a high confidence threshold where precision in testing exceeded 98 percent. Organization-wide removal stays manual.

From a security perspective, one more test belongs here: adversarial evaluation. Before launch, the red team tries to evade the model with techniques attackers actually use, such as homoglyph domains, zero-width characters, text hidden in HTML, and lures rewritten by a language model. A model that is only tested on yesterday's attacks has only been tested against yesterday's attackers.

## 7. Deployment: controlled interfaces, not direct access

The guiding principle of secure AI deployment is simple: instead of allowing direct access to the model, users and applications communicate through controlled interfaces. Veltrax follows five steps.

- **Deploy behind secure APIs.** The model runs as an internal service with mutual TLS and authenticated service identities. Nobody calls the model file directly.
- **Integrate with email systems.** The mail platform sends message metadata and content to the API and receives a score and a recommended action. The integration account gets only the permissions it needs for the actions the use case approved, for example moving mail to quarantine, but not deleting mail across all mailboxes.
- **Protect model access.** The model artifact in the registry is signed, access is limited to the deployment pipeline, and the weights are classified as confidential intellectual property. A stolen phishing model is also an attacker's test lab for evasion.
- **Implement usage controls.** Rate limits and quotas per client protect availability and make model extraction harder, because an attacker who can query a model thousands of times can probe its decision boundary or approximate a copy of it.
- **Establish logging and auditing.** Every request, score, action and model version is logged and forwarded to the SIEM. When a manager asks why an important customer email ended up in quarantine, the answer is in the log, not in somebody's memory.

Notice that none of these steps is AI-specific magic. They are API security, least privilege, secrets management and logging, applied to a new kind of asset.

## 8. Validation: can we safely operate this in the real business?

Evaluation in the lab asks whether the model works. Validation asks a harder question: can we safely operate this model in the real business? Lab data is clean and frozen; production is messy and alive.

Veltrax validates in two steps.

- **Testing in production-like conditions.** The model is connected to a staging copy of the mail flow with realistic volume, real attachment types and the real latency budget of the gateway. Several problems only show up here: very large emails time out, and some newsletter templates trigger false alarms that never appeared in the test set.
- **Shadow and canary deployment.** For three weeks the model runs in shadow mode: it scores every incoming email, but its verdicts are only logged, never acted on. Analysts compare its decisions with the existing gateway and with confirmed incidents. After that, a canary deployment enables quarantine for 5 percent of mailboxes, starting with the security team itself, before a gradual rollout.

During both phases the team does three things:

- **Validate security controls:** confirm that the API rejects unauthenticated calls, that rate limits work, that logs arrive in the SIEM and that the integration account cannot do more than intended.
- **Compare results to baselines:** is the model actually better than the current gateway rules, and for which kinds of attack?
- **Confirm operational readiness:** is there a runbook, an on-call owner, a rollback procedure and a clear fallback if the service is unavailable?

Shadow mode is one of the most underused practices in AI security. It costs little, it creates real evidence, and it lets you discover failure modes before they affect a single employee.

## 9. Maintenance and monitoring: keeping trust justified

Going live is the beginning of the expensive part. Two disciplines keep the model safe after launch.

### Maintenance

- **Maintain infrastructure:** keep the serving platform, its hosts and containers running and supported.
- **Patch frameworks and libraries:** machine learning serving frameworks and their dependencies receive security fixes like any other software. An unpatched inference server is an unpatched server.
- **Protect model artifacts:** keep weights, tokenizers and configuration in a signed, access-controlled registry, and verify signatures at load time. This is how you protect the AI itself.
- **Review security controls:** confirm periodically that permissions, rate limits and logging still work as designed. Integrations tend to accumulate rights over time.
- **Preserve operational resilience:** decide in advance what happens when the model fails. At Veltrax, if the scoring service is unavailable, mail continues to flow through the classic gateway rules and the SOC is alerted. A deliberate fallback beats an improvised one at 2 a.m.

### Monitoring

- **Monitor prediction quality:** track precision and recall on analyst-confirmed cases every week.
- **Detect data and concept drift:** data drift means the inputs change, for example when a new email platform changes header formats. Concept drift means the relationship between inputs and the right answer changes, for example when attackers move from links to QR codes, or start using language models to write flawless lures. Both silently erode accuracy.
- **Watch for abnormal behavior:** a sudden drop in phishing detections can look like good news but may mean an evasion technique is working. A single client sending thousands of unusual queries may be probing the model.
- **Measure operational performance:** latency, error rates and throughput, because a slow model gets bypassed by frustrated engineers.
- **Identify emerging risks:** feed new threat intelligence and red team findings back into the test set, so evaluation stays current.

The key mindset: trust in a model is not a one-time decision. Monitoring is how you keep that trust justified.

## 10. Feedback and iteration: improving without losing control

The loop closes with feedback, and Veltrax runs it as a five-step cycle.

- Capture analyst feedback. When analysts review flagged emails, they confirm the model was right, mark an alert as a false positive, or point out a pattern the model misunderstood. That feedback is valuable because analysts bring context the model does not have. An email may look harmless in isolation but suspicious next to a failed logon from the same country an hour earlier.
- Review user-reported misses. When an employee reports a phishing email the model let through, that is the most important signal in the whole system. Each confirmed miss is analyzed for its root cause.
- Feed lessons into the improvement cycle. Confirmed cases enter the next training data set, and recurring misses become new test cases.
- Protect feedback from manipulation. Feedback is training data in waiting, which makes it an attack surface. An attacker with access to a compromised mailbox could repeatedly mark their own phishing as "not junk", or flood the report button to drown the signal. Veltrax only accepts feedback from authenticated users, weights it by role, requires analyst confirmation before anything becomes a label, and watches for unusual feedback patterns.
- Iterate without losing control. Every retrained model is a new version that goes through evaluation, shadow mode and approval again. The previous version stays available for an immediate rollback.

The last step deserves emphasis. Continuous learning without change control is just continuous risk. A model that updates itself from unverified feedback can be steered by whoever controls the feedback.

## 11. Human-centric AI: answering the "should" question

We now return to the second question from the introduction. Three design principles shape the answer.

- AI supports human decision-making. The purpose of the Veltrax model is to help the security team process more information, identify threats faster and make better decisions. It is not intended to replace people.
- Humans remain accountable. If the model misses a phishing email, blocks an important customer message or makes a wrong recommendation, responsibility still belongs to the organization and its people. "The AI did it" is not an acceptable incident report.
- Human involvement reduces operational risk. People can monitor, review and intervene when appropriate. Users are also more likely to trust systems that are transparent, accountable and designed with human involvement in mind.

In practice, "human involvement" means three different things, and it helps to keep them apart.

### Human in the loop

Human approval is required, and critical actions require review before they happen. At Veltrax, removing an email from all 4,000 mailboxes or blocking a supplier's domain only happens after an analyst approves the model's recommendation. The model prepares the decision; a person makes it.

### Human oversight

Here the AI acts on its own, but within boundaries. Humans supervise operations, can intervene, and the system is continuously monitored, so that efficiency and risk stay balanced. Automatic quarantine at Veltrax works this way: the model acts in real time, the SOC sees every action on a dashboard, users can request release, and an analyst can switch the model back to advisory mode with a single toggle if something looks wrong.

### Human validation

Human validation is less about daily operations and more about long-term quality assurance. Once a month, two analysts review a random sample of 200 scored emails without seeing the model's verdict first. The review covers periodic checks of outputs, quality and accuracy, drift and bias, for example whether emails written in a particular language are flagged more often than they should be, and evidence for audits and compliance. Trust is difficult to build and easy to lose. Regular human review is how you make sure confidence remains justified.

One honest warning: a human in the loop only helps if the human actually thinks. Research on automation bias shows that people tend to over-trust automated recommendations, especially under time pressure. If analysts approve 500 recommendations a day, approval becomes a reflex. Show the evidence behind each verdict, keep approval volumes realistic, and measure how often humans override the model. An override rate of zero is not a sign of a perfect model. It is a sign that oversight has stopped working.

## 12. Connecting the lifecycle to established frameworks

Every stage above is reflected in frameworks that already exist. You do not need to adopt all of them, but knowing which one answers which question saves a lot of time.

- Guidelines for Secure AI System Development (UK NCSC, US CISA and international partners). Structured around four lifecycle phases: secure design, secure development, secure deployment, and secure operation and maintenance. It is the most direct match for the lifecycle in this article and a good starting checklist for any project team.
- NIST AI Risk Management Framework. Its four functions map naturally onto the loop: Govern (ownership, authority tiers, accountability), Map (use case, context and data sources), Measure (evaluation, adversarial testing, validation) and Manage (monitoring, response, iteration).
- NIST SP 800-218A. Extends the Secure Software Development Framework with practices for generative AI and dual-use foundation models, covering training data protection, model integrity and supply chain controls.
- ISO/IEC 42001 and ISO/IEC 5338. ISO/IEC 42001 defines an AI management system with controls across the AI lifecycle. ISO/IEC 5338 describes AI system life cycle processes, building on the established software and systems engineering standards.
- OWASP Machine Learning Security Top 10 and OWASP Top 10 for LLM Applications. Catalogues of the most common technical weaknesses, from data poisoning and model theft to excessive agency, which is exactly the risk the Veltrax authority tiers are designed to limit.
- MITRE ATLAS. Documents adversary tactics and techniques against AI systems. Use it to plan red team tests for the evaluation and validation stages.
- EU AI Act. For high-risk AI systems it requires a risk management system across the lifecycle (Article 9), data governance (Article 10), human oversight (Article 14), and appropriate accuracy, robustness and cybersecurity (Article 15), plus post-market monitoring. A phishing filter is usually not a high-risk system under the Act, but its requirements are a useful benchmark for good practice.

### A simple mapping for the Veltrax project

- **Business use case:** NIST AI RMF Govern and Map; NCSC/CISA secure design; authority tiers documented in the ISO/IEC 42001 management system.
- **Data collection and preparation:** EU AI Act data governance principles; OWASP data poisoning guidance; NIST SP 800-218A training data protection.
- **Model development:** NIST SP 800-218A and NCSC/CISA secure development; supply chain controls for libraries and base models.
- **Evaluation and validation:** NIST AI RMF Measure; adversarial test cases derived from MITRE ATLAS.
- **Deployment and maintenance:** NCSC/CISA secure deployment and operation; classic controls for API security, access management and patching.
- **Monitoring, feedback and human oversight:** NIST AI RMF Manage; EU AI Act human oversight principles; periodic human validation as audit evidence.

## Closing thoughts

Whether an AI system can perform a task is a question for data scientists, and it gets answered relatively early. Whether it should be trusted with a given level of authority is a question for the whole organization, and it has to be answered again and again, at every turn of the lifecycle.

The Veltrax example shows what that looks like in practice. Authority is defined before the first line of code. Data is treated as untrusted until verified. The model is evaluated on how it fails, not only on how often it succeeds. It goes live in shadow mode, behind controlled interfaces, with a fallback and a rollback. Feedback is protected like training data, because that is what it becomes. And humans stay accountable, with oversight that is measured rather than assumed.

None of this is exotic. It is good security engineering applied consistently to a new kind of system. The organizations that get AI right will not be the ones with the most advanced models, but the ones whose controls still work on the day the model is wrong.

Where in the lifecycle do you see the biggest gaps in your organization today? I would be glad to hear your experience.

---

Kind regards,\
Tom Wechsler

[Online Workshops](https://github.com/tomwechsler/Online_Workshops)

*Veltrax Logistics is a fictional company used for illustration. Figures in the example are illustrative, not measured results.*

## Sources

AI was used for spell-checking. The content is taken from my own PowerPoint files and from the following documentation:

- [NIST AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST AI 600-1, Generative Artificial Intelligence Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [NIST AI 100-2 E2025, Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf)
- [OWASP GenAI Security Project, Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
- [OWASP LLM01: Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- OWASP Top 10 for LLM Applications 2025, including LLM04:2025 Data and Model Poisoning and LLM08:2025 Vector and Embedding Weaknesses.
- [MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems)](https://atlas.mitre.org/)
- [ISO/IEC 42001:2023, Artificial intelligence management system](https://www.iso.org/standard/42001)
- ISO/IEC 5338, AI system life cycle processes.
- ISO/IEC 5259-1:2024, Data quality for analytics and machine learning, Part 1.
- European Union, Regulation (EU) 2024/1689 (Artificial Intelligence Act), in particular Articles 9, 10, 14 and 15: [EU Artificial Intelligence Act](https://artificialintelligenceact.eu/)
- Coalition for Content Provenance and Authenticity, [C2PA Specifications](https://c2pa.org/specifications/specifications/2.2/index.html)
- Google DeepMind, [SynthID](https://deepmind.google/technologies/synthid/)
- OASIS Open, STIX and TAXII.
- OWASP CycloneDX, [Machine Learning Bill of Materials (ML-BOM)](https://cyclonedx.org/capabilities/mlbom/)
- Vaswani et al., ["Attention Is All You Need" (2017)](https://arxiv.org/abs/1706.03762)
- Goodfellow et al., ["Generative Adversarial Networks" (2014)](https://arxiv.org/abs/1406.2661)

**Tags:** #Cybersecurity #ArtificialIntelligence #AISecurity #MachineLearning #MLOps #SecureByDesign #HumanInTheLoop #AIGovernance #PhishingDetection #NISTAIRMF #ISO42001 #EUAIAct #MITREATLAS #OWASP #RiskManagement #TrustworthyAI
