# 0x08. Networking Basics 2

`0x07` was about *understanding* networking concepts. This module is about actually **touching** the network configuration of a live machine — editing name resolution, inspecting real interfaces, and opening a listening port. It's a short module, but each task is a genuinely common, practical operation you'll perform on real servers.

## Task-by-Task Breakdown

### 0. `0-change_your_home_IP` — done
**Concept:** editing `/etc/hosts` to override DNS resolution locally

```bash
echo "127.0.0.1 localhost" >> /etc/hosts
echo "::1 localhost" >> /etc/hosts
echo "8.8.8.8 facebook.com" >> /etc/hosts
```
`/etc/hosts` is checked **before** any DNS server is queried — it's the machine's own local, manual override table for "hostname → IP" resolution. Adding an entry here means the machine will resolve that hostname to whatever IP you specify, regardless of what the real DNS record says.

This is a genuinely important thing to understand for two reasons: first, it's an incredibly useful tool during development and testing (pointing a domain at a local or staging server before DNS is updated, without needing to touch a real DNS provider). Second, it's exactly the mechanism attackers exploit to redirect traffic silently (hence why this file is one of the first things checked when a machine's behavior seems suspicious — "is this hostname actually resolving where it should be?"). Editing `/etc/hosts` requires root, since it directly controls how the whole machine sees the network.

### 1. `1-show_attached_IPs` — done
**Commands used:** `ifconfig` (or `ip addr`), filtered with `grep`/`awk`

```bash
ifconfig | grep "inet " | awk '{print $2}' | grep -v "127.0.0.1"
```
Lists every **active IPv4 address** attached to the machine's network interfaces, excluding the loopback address (`127.0.0.1`, which always exists but isn't a "real" external-facing address). This combines several earlier-module skills at once: `grep` to isolate the lines that matter, `awk` to extract just the address field from each line, and a second `grep -v` to filter out the one address that isn't useful for this purpose.

In practice, this is exactly the kind of one-liner you'd run when you SSH into an unfamiliar server and need to quickly answer "what IP(s) does this machine actually have" — before you can configure a firewall rule, a load balancer target, or a DNS record pointing at it, you need to know precisely what address it's reachable on.

### 100. `100-port_listening_on_localhost` — done (bonus)
**Concept:** binding a listener to a TCP port and responding to a connection

```bash
while true; do
    echo -e "HTTP/1.1 200 OK\n\nAURORE_IS_IN_DA_PLACE" | nc -l -p 98
done
```
Opens a **listening socket** on port 98 (`nc -l`, netcat in listen mode), and when a client connects, sends back a fixed response before closing. This is a small, stripped-down illustration of what *every* network service actually is at its core: a program bound to a port, waiting for a connection, and responding when one arrives — the same fundamental pattern behind Nginx on port 80, MySQL on port 3306, or SSH on port 22, just without any of the real protocol logic layered on top.

Wrapping it in a loop (`while true`) matters: a single `nc -l` call handles exactly one connection and then exits — the loop is what makes it behave like a persistent service that can accept connection after connection, rather than a one-shot script.

---

## Skills Demonstrated in This Module

- **Local DNS overrides**: editing `/etc/hosts` and understanding its precedence over real DNS resolution
- **Interface inspection**: extracting a machine's actual IP addresses from `ifconfig`/`ip addr` output using text-processing tools from earlier modules
- **Basic socket behavior**: what "listening on a port" actually means in practice, using `nc` as a minimal stand-in for a real service
- **Combining tools across modules**: this whole module is really `0x02`/`0x03`'s text-processing skills applied specifically to networking output

## Why This Matters Beyond the Exercises

Editing `/etc/hosts` for local testing, checking a server's real IP before configuring DNS or a firewall, and understanding that "a service" is fundamentally just "something listening on a port" are all things that come up constantly — in local development, in staging environments, and when diagnosing "why can't this connect" during an incident. This module turns the theory from `0x07` into commands you'd actually type on a real box.

## Requirements

- Ubuntu 16.04/20.04 LTS
- `net-tools` (for `ifconfig`) or `iproute2` (for `ip`)
- `netcat` (`nc`)
- Root/sudo access for editing `/etc/hosts`

## Author

**SwissKnifeTech** — ALX System Engineering & DevOps track
