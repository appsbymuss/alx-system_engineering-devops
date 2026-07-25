# ALX System Engineering & DevOps
 
Hi, I'm SwissKnifeTech 
 
This repository documents my journey through the **System Engineering & DevOps** track at ALX (in partnership with Holberton School). It's not just a collection of scripts — it's a record of how I went from writing my first `chmod` command to configuring load balancers, debugging live web stacks, and writing postmortems for production incidents.
 
I'm sharing it as-is (including the messy early commits) because I think the progression tells a more honest story than a polished final product would. Below, I explain **what each module taught me and why it matters**, not just what folder it lives in.
 
## Why This Track
 
Before you can build reliable software, you need to understand the systems it runs on: how a Linux server boots, how processes talk to each other, how a request travels from a browser to a server and back, and what happens when any part of that chain fails. This repository is my proof of that understanding — built one project at a time.
 
## Table of Contents & What I Learned
 
### Foundations: Shell & Linux
| Directory | What it covers | Why it matters |
|---|---|---|
| [0x00-shell_basics](./0x00-shell_basics) | Navigating the filesystem, running commands, understanding the shell environment | The baseline for everything else — you can't automate what you don't understand manually first |
| [0x01-shell_permissions](./0x01-shell_permissions) | Unix permissions model (owner/group/other), `chmod`, `chown`, symbolic vs. octal notation | Misconfigured permissions are a classic source of security incidents — I learned to reason about *who* can do *what* to a file, and why |
| [0x02-shell_redirections](./0x02-shell_redirections) | stdin/stdout/stderr, pipes, redirection operators, combining filters | This is how Unix tools compose into pipelines — the core idea behind most CLI-based automation |
| [0x03-shell_variables_expansions](./0x03-shell_variables_expansions) | Environment vs. shell variables, `PATH`, `$?`, quoting rules | Understanding variable scope and expansion is what separates a script that "usually works" from one that's predictable |
| [0x04-loops_conditions_and_parsing](./0x04-loops_conditions_and_parsing) | `for`/`while`/`until` loops, `if`/`case` statements, shebangs, generating SSH keys | Turning repetitive manual tasks into scripts — the first real step into automation |
| [0x05-processes_and_signals](./0x05-processes_and_signals) | PIDs, `ps`, `pgrep`, `pkill`, signal handling (`SIGTERM`, `SIGKILL`, etc.) | Every running service is a process — knowing how to inspect and control them safely is essential for operating a server |
| [0x06-regular_expressions](./0x06-regular_expressions) | Pattern matching with `sed` and regex | Parsing and transforming text reliably, without hand-editing files |
 
### Networking
| Directory | What it covers | Why it matters |
|---|---|---|
| [0x07-networking_basics](./0x07-networking_basics) | `localhost`/`127.0.0.1`, `0.0.0.0`, `/etc/hosts`, network interfaces | The building blocks of how machines find and talk to each other |
| [0x08-networking_basics_2](./0x08-networking_basics_2) | Routing, gateways, listening ports, basic diagnostics | Diagnosing "why can't this machine reach that one" is a daily DevOps skill |
| [0x11-what_happens_when_your_type_google_com...](./0x11-what_happens_when_your_type_google_com_in_your_browser_and_press_enter) | Full request lifecycle: DNS resolution, TCP/IP, TLS handshake, HTTP request/response, rendering | I had to explain, end-to-end, every layer a request passes through — this project ties networking, security, and web serving into one coherent mental model |
 
### Infrastructure & Configuration Management
| Directory | What it covers | Why it matters |
|---|---|---|
| [0x0A-configuration_management](./0x0A-configuration_management) | Infrastructure as code with Puppet | Manually configuring servers doesn't scale — this is where I started treating infrastructure the way developers treat code: version-controlled and repeatable |
| [0x0B-ssh](./0x0B-ssh) | Key-based authentication, SSH config files, connecting without passwords | Secure, auditable remote access — the backbone of managing any real server fleet |
| [0x0C-web_server](./0x0C-web_server) | Installing and configuring Nginx | Serving a website is more than `apt install` — it's understanding server blocks, ports, and how requests get routed |
| [0x0F-load_balancer](./0x0F-load_balancer) | HAProxy configuration, round-robin distribution | Scaling beyond one server means distributing traffic intelligently — and understanding the tradeoffs of different balancing algorithms |
| [0x10-https_ssl](./0x10-https_ssl) | TLS certificates, HTTPS termination | Encrypting traffic in transit, and understanding why "just add HTTPS" involves certificate chains and termination points |
| [0x13-firewall](./0x13-firewall) | UFW rules, opening/closing ports | Security starts with controlling what's exposed — I learned to reason about least-privilege network access |
| [0x1A-application_server](./0x1A-application_server) | Deploying an app server (Gunicorn) behind Nginx via Puppet | Bringing everything together: reverse proxy + application server + automated configuration |
 
### Data & APIs
| Directory | What it covers | Why it matters |
|---|---|---|
| [0x14-mysql](./0x14-mysql) | MySQL installation, users, privileges, backups | Data persistence and access control — the parts of a stack that are hardest to recover from if done wrong |
| [0x15-api](./0x15-api) | Consuming REST APIs, parsing JSON responses | Most modern systems talk to each other over HTTP APIs — this is that skill in practice |
| [0x16-api_advanced](./0x16-api_advanced) | Pagination, rate limiting, recursive API calls | Real-world APIs aren't a single request — they require handling limits and incomplete data gracefully |
 
### Operating & Debugging Production Systems
| Directory | What it covers | Why it matters |
|---|---|---|
| [0x0D-web_stack_debugging_0](./0x0D-web_stack_debugging_0) | Diagnosing a broken web server via SSH, no GUI | Debugging blind, using only logs and command-line tools, is a core SRE skill |
| [0x0E-web_stack_debugging_1](./0x0E-web_stack_debugging_1) | Deeper Nginx/process-level debugging | Building the habit of forming a hypothesis, testing it, and narrowing down root cause systematically |
| [0x12-web_stack_debugging_2](./0x12-web_stack_debugging_2) | Debugging a multi-service failure | Real outages rarely have one obvious cause — this taught me to check the whole chain, not just the first suspect |
| [0x17-web_stack_debugging_3](./0x17-web_stack_debugging_3) | Debugging under added complexity/constraints | Reinforcing the debugging process under pressure and ambiguity |
| [0x18-webstack_monitoring](./0x18-webstack_monitoring) | Setting up monitoring agents (e.g. Sumologic) and collecting metrics | You can't fix what you can't see — this is where I moved from reactive debugging to proactive visibility |
| [0x19-postmortem](./0x19-postmortem) | Writing a real postmortem document for a simulated outage | Technical writing is part of the job — clearly documenting what broke, why, and how to prevent it is as important as fixing it |
| [0x1B-web_stack_debugging_4](./0x1B-web_stack_debugging_4) | Final, most complex debugging scenario | Combining everything above under a realistic, multi-layered failure |
 
### Security
| Directory | What it covers | Why it matters |
|---|---|---|
| [attack_is_the_best_defense](./attack_is_the_best_defense) | Basic offensive techniques used to inform defensive configuration | Understanding how a system can be attacked is what makes hardening it meaningful, rather than just following a checklist |
 
## Skills This Repository Demonstrates
 
- **Shell scripting** in Bash, following defensive scripting practices (quoting, exit codes, error handling)
- **Linux system administration**: permissions, processes, users, services
- **Networking fundamentals**: from `/etc/hosts` up to the full DNS → TCP → TLS → HTTP request lifecycle
- **Infrastructure as code** with Puppet — treating server configuration as version-controlled, repeatable code
- **Web infrastructure**: Nginx, HAProxy, HTTPS/SSL, UFW firewalls
- **Databases**: MySQL setup, users, and privilege management
- **API integration**: REST, JSON, pagination, and rate-limit-aware requests
- **Incident response**: structured debugging methodology and postmortem writing
- **Security fundamentals**: least-privilege access and basic attack/defense reasoning
## Requirements
 
- Ubuntu 16.04/20.04 LTS (or later)
- Bash (`#!/usr/bin/env bash`)
- Scripts follow Shellcheck-style shell scripting conventions
## Usage
 
Each directory is self-contained with its own scripts or configuration files. To run a shell script:
 
```bash
chmod +x ./script_name
./script_name
```
 
To apply a Puppet manifest:
 
```bash
puppet apply manifest_name.pp
```
 
## A Note on the Commits
 
You'll notice commit messages like "fix chmod" and "done" scattered throughout. I've left the history as it happened rather than rewriting it — it reflects the iterative, sometimes messy reality of learning system administration by actually doing it, not just reading about it.
 
## Author
 
**SwissKnifeTech**
Built as part of the ALX Software Engineering program (System Engineering & DevOps specialization).
 
## License
 
Provided for educational purposes as part of the ALX curriculum.
