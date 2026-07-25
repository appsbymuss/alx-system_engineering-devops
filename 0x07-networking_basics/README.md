# 0x07. Networking Basics

This module is a shift in focus from the previous ones: instead of writing scripts, most of these tasks are **conceptual** — answering specific questions about how networks actually work. That's deliberate. You can memorize `ping` and `curl` commands without understanding what's happening underneath them, but you can't *debug* a real networking problem that way. This module is where I built the mental model that the later, hands-on networking and debugging modules (`0x08`, `0x11`, `0x0F` load balancing, `0x10` HTTPS) all depend on.

## Why This Module Matters

Almost every production incident that isn't a code bug is a networking problem in disguise: a service that "isn't responding" might be down, or it might be a firewall rule, a DNS issue, a routing problem, or the wrong port. Without a real model of how data actually moves between machines, every one of those looks identical from the outside — "it doesn't work." This module is what makes them distinguishable.

---

## Task-by-Task Breakdown

### 0. `0-OSI_model` — The seven-layer map
**Concept:** the OSI (Open Systems Interconnection) model — a conceptual framework describing how data moves through **seven layers**, from physical signals to the application a user actually interacts with:

| Layer | Name | Example |
|---|---|---|
| 7 | Application | HTTP, DNS, SSH |
| 6 | Presentation | Encryption, encoding (TLS) |
| 5 | Session | Session establishment/management |
| 4 | Transport | TCP, UDP |
| 3 | Network | IP, routing |
| 2 | Data Link | MAC addresses, switches |
| 1 | Physical | Cables, radio signals, electrical pulses |

This task asks which layer specific devices operate at — e.g. a **switch** operates at Layer 2 (it forwards traffic based on MAC addresses), while a **router** operates at Layer 3 (it forwards traffic based on IP addresses), and a **firewall** can operate at multiple layers depending on what it's inspecting. Knowing *which layer* a problem lives at is the fastest way to narrow down a networking issue — a Layer 2 problem (cabling, switch) and a Layer 7 problem (the application itself) need completely different troubleshooting approaches.

### 1. `1-types_of_network` — LAN vs. WAN
**Concept:** classifying networks by scale and ownership.

- **LAN (Local Area Network)** — a network confined to one physical location (an office, a data center rack), typically owned and controlled entirely by one organization.
- **WAN (Wide Area Network)** — a network spanning multiple physical locations, often crossing infrastructure owned by third parties (ISPs). The public internet is effectively the largest WAN there is.

Why it matters: LAN traffic is fast and (usually) trusted; WAN traffic is slower, less predictable, and needs to be treated as untrusted by default. Architectural decisions — where you place a database, whether you need a VPN, how much latency to expect — all start with this distinction.

### 2. `2-MAC_and_IP_address` — Two different kinds of "address"
**Concept:** the difference between a **MAC address** and an **IP address**, and why a device needs both.

- A **MAC address** is a hardware identifier burned into a network interface — fixed, and only meaningful on the *local* network segment (Layer 2).
- An **IP address** is a logical, assignable address used to route traffic *between* networks (Layer 3) — and can change (DHCP, moving networks, cloud IP reassignment).

The practical distinction: your laptop's MAC address never changes no matter what Wi-Fi network you join, but its IP address changes every time, because MAC identifies the *physical device* and IP identifies its *current location on a network*.

### 3. `3-UDP_and_TCP` — Reliable vs. fast
**Concept:** the two dominant Layer 4 (Transport) protocols, and the tradeoff between them.

- **TCP** (Transmission Control Protocol) is **connection-oriented** and **reliable** — it establishes a handshake before sending data, guarantees packets arrive in order, and retransmits anything lost. The cost is overhead and latency.
- **UDP** (User Datagram Protocol) is **connectionless** — it just sends packets with no handshake, no ordering guarantee, and no retransmission. The benefit is speed and lower overhead.

Why it matters: TCP is what you want when correctness matters more than speed (web pages, file transfers, database connections — you can't have a webpage arrive with paragraphs missing). UDP is what you want when speed matters more than perfect delivery (video calls, live streaming, DNS lookups — a dropped video frame is better than a frozen call waiting for a retransmit).

### 4. `4-TCP_and_UDP_ports` — Ports as addressed mailboxes
**Concept:** a **port** is a number that identifies *which service* on a machine a piece of traffic is meant for — the IP address gets you to the right machine, the port gets you to the right application on it.

Common ports worth knowing cold:
| Port | Protocol | Service |
|---|---|---|
| 22 | TCP | SSH |
| 53 | TCP/UDP | DNS |
| 80 | TCP | HTTP |
| 443 | TCP | HTTPS |
| 3306 | TCP | MySQL |

This is directly practical knowledge: firewall rules, load balancer configs, and Docker port mappings are all just decisions about "which port maps to which service," and misreading a port number is a genuinely common source of "why can't I connect" issues.

### 5. `5-is_the_host_on_the_network` — done (script)
**Command used:** `ping`

```bash
#!/usr/bin/env bash
ping -c 3 "$1"
```
The one hands-on script in the module: taking everything above and applying it with the most basic network diagnostic tool there is. `ping` sends ICMP echo requests to a target and reports whether (and how quickly) it responds. `-c 3` limits it to 3 attempts instead of running forever. It's the very first command any real troubleshooting session reaches for — "is the host even reachable at all" — before investigating anything more specific like a particular port or service.

---

## Skills Demonstrated in This Module

- **Layered thinking**: mapping a networking problem to the correct OSI layer before troubleshooting it
- **Network topology awareness**: distinguishing LAN from WAN, and why that changes trust and performance assumptions
- **Addressing models**: understanding MAC vs. IP addresses as two different, complementary identification systems
- **Transport protocol tradeoffs**: TCP's reliability vs. UDP's speed, and picking the right one for a given use case
- **Port fluency**: recognizing standard service ports on sight
- **Basic connectivity diagnostics**: `ping` as the first tool in any network troubleshooting sequence

## Why This Matters Beyond the Exercises

This module is the conceptual foundation for every hands-on networking task later in the track — configuring a load balancer (`0x0F`) means nothing if you don't understand TCP; setting up HTTPS (`0x10`) means nothing without understanding what layer TLS operates at; debugging "the site is down" (`0x0D`–`0x1B`) always starts with the same layered troubleshooting instinct this module builds: is it physical, is it addressing, is it the transport, or is it the application?

## Requirements

- Ubuntu 16.04/20.04 LTS
- `ping` (part of `iputils-ping`, installed by default on most distributions)

## Author

**SwissKnifeTech** — ALX System Engineering & DevOps track
