# 0x0B. SSH

SSH (Secure Shell) is how almost every real server gets managed — you don't walk up to a data center rack, you connect remotely, over an encrypted channel, and authenticate without ever typing a password over the wire. This module builds on `0x04`'s `ssh-keygen` task and turns it into actual, working remote access: generating real keypairs, connecting with them, and configuring the client so connecting is fast and repeatable instead of a long command you retype every time.

## The Core Concept: Key-Based Authentication

SSH supports password authentication, but real infrastructure almost never uses it — for a good reason. A keypair consists of:
- A **private key** — stays on your machine, never shared, ideally protected further by a passphrase
- A **public key** — copied to any server you want to access, added to that server's `~/.ssh/authorized_keys`

When you connect, the server challenges your client to prove it holds the private key matching a public key it already trusts — without the private key ever leaving your machine, and without a password ever being transmitted. This is both more secure (nothing to intercept, nothing to brute-force) and more automatable (a script can authenticate without a human typing a password).

---

## Task-by-Task Breakdown

### 0. `0-use_a_private_key` — done (fix commit included)
**Command used:** `ssh -i`

```bash
ssh -i ~/.ssh/school -o StrictHostKeyChecking=no ubuntu@<server-ip>
```
The `-i` flag tells `ssh` explicitly which private key file to use for authentication, instead of relying on its default search order (`~/.ssh/id_rsa`, etc.) — necessary whenever you're managing multiple servers with different, purpose-specific keys rather than one universal key for everything. `StrictHostKeyChecking=no` skips the interactive "are you sure you want to continue connecting" prompt — convenient for scripting and first-time automated connections, though worth knowing it also means you're not manually verifying the server's host key, which matters more in genuinely untrusted network conditions than in a controlled lab environment.

Worth noting honestly: the commit history for this exact task shows a config fix for a new server — a very true-to-life detail. SSH configuration is exactly the kind of thing that looks done until you point it at a different host and discover a path, key, or username assumption that doesn't hold anymore.

### 1. `1-create_ssh_key_pair` — done
**Command used:** `ssh-keygen`

```bash
ssh-keygen -f ~/.ssh/school -t rsa -b 4096 -N ""
```
Generates a fresh RSA keypair, non-interactively (empty passphrase via `-N ""`, matching the pattern from `0x04`), named specifically (`-f ~/.ssh/school`) rather than overwriting the account's default key. Using named, purpose-specific keys per server or per project — instead of one shared key for everything — is a genuinely good practice: it means revoking access to one server (by removing that one public key) doesn't require regenerating and redistributing a key used everywhere else.

### 2. `2-ssh_config` — done (fix commit included)
**Concept:** the SSH client configuration file (`~/.ssh/config`)

```
Host school
    HostName <server-ip>
    User ubuntu
    IdentityFile ~/.ssh/school
    StrictHostKeyChecking no
    PasswordAuthentication no
```
`~/.ssh/config` lets you define a **shortcut** (`Host school`) that bundles the hostname, username, and key file together, so `ssh school` does everything `ssh -i ~/.ssh/school ubuntu@<ip>` would have required typing out in full. This is the exact mechanism that makes managing several servers day-to-day practical — instead of memorizing or looking up IPs and key paths every time, each server gets a short, memorable alias. `PasswordAuthentication no` is a meaningful security setting too: it disables the fallback to password login entirely for this host, enforcing key-only access even if the server itself would technically still accept a password.

### 100. `100-puppet_ssh_config.pp` — done (bonus)
**Concept:** managing the SSH config file *declaratively*, with Puppet

```puppet
file { '/root/.ssh/config':
  ensure  => present,
  content => "Host school\n    Hostname <server-ip>\n    User ubuntu\n    IdentityFile ~/.ssh/school\n    StrictHostKeyChecking no\n",
}
```
Ties this module directly back to `0x0A`: instead of manually creating or editing `~/.ssh/config`, a Puppet `file` resource ensures the correct config content is always in place. This is exactly how real infrastructure teams manage SSH access at scale — the config file itself becomes part of a server's provisioning, guaranteed consistent every time a machine is set up or re-applied, instead of something a human configures by hand and might get slightly wrong on the tenth server.

---

## Skills Demonstrated in This Module

- **Key-based authentication**: understanding *why* it replaces passwords, not just how to run the command
- **Explicit key selection**: `ssh -i`, and managing multiple purpose-specific keypairs instead of one shared key
- **Client-side configuration**: `~/.ssh/config` host aliases, and the specific settings (`IdentityFile`, `User`, `StrictHostKeyChecking`, `PasswordAuthentication`) that control connection behavior
- **Bringing configuration management into security-relevant setup**: using Puppet (from `0x0A`) to manage SSH configuration declaratively, rather than by hand

## Why This Matters Beyond the Exercises

Every single hands-on infrastructure module later in this repository — web servers, load balancers, application servers, debugging exercises — assumes you can already get onto the target machine reliably and securely. This module is genuinely the connective tissue of the whole repo: it's not a standalone topic, it's the access layer every other module depends on silently.

## Requirements

- Ubuntu 16.04/20.04 LTS
- OpenSSH client (`ssh`, `ssh-keygen`)
- Puppet, for the bonus task

## Author

**SwissKnifeTech** — ALX System Engineering & DevOps track
