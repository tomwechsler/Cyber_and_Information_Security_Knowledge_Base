# The Critical Role of Baselines in Cybersecurity!

## Introduction:
In cybersecurity, you cannot protect what you do not understand, and you cannot detect what you cannot measure. Baselines provide a trusted reference point that defines what “normal” looks like for systems, networks, and user behavior. Without established baselines, organizations struggle to identify misconfigurations, detect anomalies, and respond effectively to threats. As cyberattacks grow more sophisticated, baselines become a foundational element of any mature cybersecurity program.

## Understanding Baselines Through a Physical Server Example

To understand why baselines are so important in cybersecurity, it helps to look at a simple and concrete example: a physical server.

Imagine a newly installed physical server in a data center. The operating system has just been deployed, required services are installed, security patches are up to date, and the system has been hardened according to best practices (for example, using CIS Benchmarks). At this point, the server is in a **known, trusted, and approved state**. This state becomes the **baseline**.

What if the server has been running for a long time? What is “normal” now, or what behavior can be expected?

Is that normal?

<img src="/Images/_base01.png" alt="CPU" width="500"/>

Or that?

<img src="/Images/_base02.png" alt="Memory" width="500"/>

Or that?

<img src="/Images/_base03.png" alt="Ethernet" width="500"/>

**It's quite simple: we don't know. The necessary reference values are missing!**  

### What Does the Baseline Include?

A baseline for a physical server typically defines:

- Installed operating system and version  
- Approved services and running processes  
- User and administrator accounts  
- Security configurations (firewall rules, logging, authentication settings)  
- Patch level and firmware versions  
- Performance metrics such as CPU, memory, disk usage, and network activity  

This baseline answers a critical question: **“What does normal look like for this system?”**

---

## Let's set up a baseline together with “Perfmon” (this is only an example configuration).  This is by no means a final or absolutely complete configuration.

1. I am using Windows Server 2022 here (also works with Windows 11). Navigate to Start, then right-click and enter “perfmon.”

<img src="/Images/_base04.png" alt="Perfmon" width="500"/>

2. Start a new Data Collector set

<img src="/Images/_base05.png" alt="Data Collector" width="500"/>

3. Please provide a name

<img src="/Images/_base06.png" alt="Give a Name" width="500"/>

4. Choose Performance counter

<img src="/Images/_base07.png" alt="Performance Counter" width="500"/>

5. Add the performance indicators of your choice

<img src="/Images/_base08.png" alt="Performance Indicators" width="500"/>

**Like this**  

<img src="/Images/_base09.png" alt="Indicators" width="500"/>

6. The report is saved in this path

<img src="/Images/_base10.png" alt="Path" width="500"/>

7. Open properties

<img src="/Images/_base11.png" alt="Properties" width="500"/>

8. Now define the schedule (e.g., weekdays during active office hours or when the system is actually needed).

<img src="/Images/_base12.png" alt="Schedule" width="500"/>

**Range**  

<img src="/Images/_base13.png" alt="Range" width="500"/>

**Stop condition**  

<img src="/Images/_base14.png" alt="Stop condition" width="500"/>

9. Once the first schedule has been executed, you can call up the report and you will have an initial baseline!

<img src="/Images/_base15.png" alt="Basline" width="500"/>

### Why the Baseline Matters

Once the server is in production, changes will inevitably occur. Patches are applied, configurations are updated, and workloads change. Without a baseline, it becomes difficult to distinguish between **authorized changes** and **potential security incidents**.

For example:
- A new service starts running that was not part of the baseline  
- CPU usage suddenly spikes outside normal operating patterns  
- A new user account appears without an approved change request  
- Firewall rules change unexpectedly  

Because a baseline exists, these deviations are immediately visible. Security teams can quickly determine whether the change is legitimate or potentially malicious. **In addition, you can restart your custom data collection set again and again and then compare the results with the existing reports!**  

### Baselines Enable Detection and Response

Baselines are fundamental for:

- **Configuration management** – detecting drift from approved settings  
- **Anomaly detection** – identifying unusual behavior  
- **Incident response** – understanding what changed and when  
- **Audits and compliance** – proving systems are configured securely  

Without a baseline, security teams are effectively working blind. They may detect that something is “wrong,” but they lack the context needed to assess impact and respond confidently.

### A Simple Rule

If you do not know the baseline state of your server, every alert becomes a guess.  
If you do know the baseline, every deviation becomes a signal.

That is why baselines are not optional—they are a foundational requirement for any effective cybersecurity program.

---
## *HAPPY BASELINING!*
---