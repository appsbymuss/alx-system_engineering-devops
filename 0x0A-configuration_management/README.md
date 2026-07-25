# 0x0A. Configuration Management

Every module before this one was about doing things **manually, on one machine, one command at a time**. This module is the turning point: instead of SSHing in and running commands by hand, you describe the **desired end state** of a system in a file, and a tool (Puppet, here) figures out how to get there — and, critically, can apply that same description to any number of servers, consistently, repeatedly, without drift.

This is the actual conceptual leap from "system administrator typing commands" to "DevOps engineer writing infrastructure as code" — and it's the foundation the rest of the infrastructure modules in this repo build on (`0x0C` web server, `0x0F` load balancer, `0x1A` application server are all deployed via Puppet manifests that build on exactly this).

## The Core Concept: Declarative, Not Procedural

A Bash script is **procedural** — it's a list of steps: do this, then this, then this. If you run it twice, it tries to do everything again, and might fail the second time (e.g. `mkdir` erroring because the directory already exists).

A Puppet manifest is **declarative** — it describes the *end state* you want ("this file should exist, with this content" / "this package should be installed"), not the steps to get there. Puppet itself figures out what needs to change to reach that state, and — critically — running it again when the system already matches the description does **nothing**, because there's nothing left to do. This property is called **idempotency**, and it's the single most important idea in this module: a well-written manifest is safe to apply over and over, on any number of machines, and it will only ever change what actually needs changing.

## Puppet Syntax Basics

A Puppet manifest (`.pp` file) is made of **resources** — the fundamental unit of Puppet's DSL:

```puppet
type { 'title':
  attribute => value,
  attribute => value,
}
```

- `type` — what kind of thing you're managing (`file`, `package`, `exec`, `service`, `user`, and many more)
- `'title'` — a unique name for this resource within the manifest
- `attribute => value` pairs — the desired properties of that resource

You apply a manifest with:
```bash
puppet apply manifest.pp
```

---

## Task-by-Task Breakdown

### 0. `0-create_a_file.pp` — done
**Resource type used:** `file`

```puppet
file { '/tmp/school':
  ensure  => present,
  content => "I love Puppet\n",
}
```
The `file` resource manages a file's existence, content, permissions, and ownership declaratively. `ensure => present` means "this file should exist" (as opposed to `absent`, which would delete it if found). This is the simplest possible demonstration of the declarative model: you're not writing "create a file," you're writing "this file should be in this state" — and Puppet handles the actual creation (or leaves it alone if it's already correct).

### 1. `1-install_a_package.pp` — done
**Resource type used:** `package`

```puppet
package { 'flask':
  ensure   => 'installed',
  provider => 'pip',
}
```
The `package` resource manages software installation across whatever package manager the system uses. The `provider` attribute tells Puppet *which* package manager to use for this specific resource — here, `pip` (Python's package manager) rather than the system's default `apt`/`yum`. This is a good early look at one of Puppet's real strengths: the same `package` resource type works across `apt`, `yum`, `pip`, `gem`, and more — you write one consistent syntax, and Puppet handles the manager-specific mechanics underneath.

### 2. `2-execute_a_command.pp` — done
**Resource type used:** `exec`

```puppet
exec { 'create_school_file':
  command => '/usr/bin/touch /tmp/school',
  unless  => '/usr/bin/test -f /tmp/school',
}
```
The `exec` resource is the escape hatch of Puppet: it runs an arbitrary shell command, for situations that don't map cleanly onto one of Puppet's purpose-built resource types. It's deliberately treated as a "last resort" resource in real Puppet usage, for a specific reason this task highlights: **`exec` isn't idempotent by default** — the command itself has no idea whether it already ran. That's exactly why the `unless` attribute matters here: it's a guard condition Puppet checks *before* running the command, skipping it entirely if the condition is already true. Without a guard like `unless` (or `onlyif`, `creates`), an `exec` resource would try to run its command on every single Puppet apply, breaking the whole idempotency model the rest of the module builds around.

---

## Skills Demonstrated in This Module

- **Declarative thinking**: describing desired end state instead of a sequence of steps
- **Idempotency**: understanding why "safe to run repeatedly" is a core requirement of real infrastructure automation, not a nice-to-have
- **Puppet resource syntax**: `type { 'title': attribute => value }`, and reading/writing it fluently
- **Choosing the right resource type**: `file` for file state, `package` (with a specific `provider`) for software installation, `exec` only when nothing more specific fits — and guarding it properly when it's used
- **Cross-platform abstraction**: understanding that `provider` lets one manifest work across different underlying package managers

## Why This Matters Beyond the Exercises

This is genuinely the mindset shift that separates "someone who can SSH in and fix a server" from "someone who can manage infrastructure at scale." Three servers, you can configure by hand. Thirty, you can't — not reliably, not consistently, not without eventually introducing drift between them. Configuration management tools like Puppet (and, in other ecosystems, Ansible, Chef, or Terraform for infrastructure itself) exist specifically to solve that problem, and this module is where I built the conceptual foundation — idempotency, declarative resources, providers — that transfers directly to any of those tools, not just Puppet specifically.

## Requirements

- Ubuntu 16.04/20.04 LTS
- Puppet (`puppet apply` must be available)

## Author

**SwissKnifeTech** — ALX System Engineering & DevOps track
