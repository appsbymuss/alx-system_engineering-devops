# 0x01. Shell Permissions

If `0x00-shell_basics` was about **moving around** a Unix system, this module is about **controlling who can do what** on it. Every file and directory on a Linux system has an owner, a group, and a permission set — and understanding that model is what separates "I can run commands" from "I understand why my command just failed with `Permission denied`."

This module matters more than it looks at first glance: the majority of real production incidents I'll eventually see in the later debugging modules of this track trace back to two things — a misconfigured service, or a permissions problem. This is where I built the mental model to diagnose the second one on sight.

## The Core Concept: Owner / Group / Other

Every file has three sets of permissions, applied to three categories of user:

| | Read | Write | Execute |
|---|---|---|---|
| **Owner (u)** | Can view the file | Can modify it | Can run it (if a script/binary) |
| **Group (g)** | Same, for anyone in the file's group | | |
| **Other (o)** | Same, for everyone else | | |

Permissions can be written **symbolically** (`u+x`, `g-w`, `o=r`) or **numerically** (`chmod 755`), where each digit is a sum: `4` = read, `2` = write, `1` = execute (so `7` = read+write+execute, `5` = read+execute, etc.). Almost every task below is really just a variation on "which of these three groups gets which of these three permissions."

---

## Task-by-Task Breakdown

### 0. `0-iam_betty` — My name is Betty
**Command used:** `su`

```bash
su betty
```
`su` (switch user) starts a new shell session as a different user — here, `betty`. This is the foundation for everything else in the module: to understand permissions, you need to actually experience a command *succeeding or failing* under a different identity, not just read about it.

### 1. `1-who_am_i` — done the job
**Command used:** `whoami`

```bash
whoami
```
Prints the username of whoever is currently running the shell. Simple, but genuinely useful — especially after chaining several `su`/`sudo` commands, when it's easy to lose track of which user you actually are.

### 2. `2-groups` — done the job
**Command used:** `groups`

```bash
groups
```
Lists every group the current user belongs to. Since group membership is one of the three permission categories (owner/**group**/other), knowing your own groups is the first step to predicting whether a given command will succeed.

### 3. `3-new_owner` — done the job
**Command used:** `chown`

```bash
chown betty hello
```
`chown` (change owner) transfers ownership of a file to another user. Only root (or the current owner, in some configurations) can do this — which is itself a security boundary: you can't just hand yourself ownership of someone else's file.

### 4. `4-empty` — done the job
**Command used:** `chmod` (numeric, all permissions removed)

```bash
chmod 0000 my_file
```
Sets **every** permission bit to off, for owner, group, and other alike. Nobody — not even the owner — can read, write, or execute the file without first changing its permissions again (or using root/sudo). This task exists to prove a point: permissions aren't just about "locking others out," they can lock out the owner too if set carelessly.

### 5. `5-execute` — done the job
**Command used:** `chmod` (symbolic, add execute)

```bash
chmod u+x my_file
```
Adds the **execute** bit for the owner only. This is the exact fix for the classic `-bash: ./script.sh: Permission denied` error — the script is readable, but the shell won't run it as a program until the execute bit is set.

### 6. `6-multiple_permissions` — done the job
**Command used:** `chmod` (multiple symbolic changes at once)

```bash
chmod u+x,g+w,o-r my_file
```
Shows that `chmod` accepts several comma-separated changes in a single call, applied to different categories at once (owner gets execute, group gets write, other loses read). This is how real permission changes are usually written — one deliberate `chmod` line rather than three separate commands.

### 7. `7-everybody` — done the job
**Command used:** `chmod` (grant to everyone)

```bash
chmod +x my_file
```
When no category (`u`/`g`/`o`) is specified, `chmod` applies the change to **all three at once** — equivalent to `chmod ugo+x`. Useful, but worth using deliberately: it's an easy way to over-grant permissions if you're not paying attention.

### 8. `8-James_Bond` — done the job
**Command used:** `chmod 007` (numeric)

```bash
chmod 007 my_file
```
A memorable (and deliberately named) example of numeric permissions: `007` means the **owner and group get nothing**, while **other** gets full read/write/execute. It's a good exercise in reading numeric mode literally, digit by digit, rather than guessing — "007" looks like a joke, but it's a real, working permission set once you decode it.

### 9. `9-John_Doe` — done the job
**Command used:** `chmod 700` (numeric)

```bash
chmod 700 my_file
```
The inverse of the previous task: the **owner** gets full read/write/execute, and group/other get nothing. This is a common real pattern for private scripts or credentials files — e.g. an SSH private key is expected to be `600` (owner read/write only), or `ssh` will refuse to use it.

### 10. `10-mirror_permissions` — done the job
**Command used:** `chmod --reference`

```bash
chmod --reference=file_1 file_2
```
Copies the exact permission set from one file onto another, instead of specifying permissions manually. Handy for keeping a batch of related files (e.g. deployment scripts) consistently permissioned without recalculating the numeric/symbolic mode each time.

### 11. `11-directories_permissions` — done the job
**Command used:** `chmod` applied to a directory

```bash
chmod u+x my_dir
```
Execute permission means something different on a **directory** than on a file: it doesn't mean "run it," it means "you're allowed to `cd` into it and access what's inside." This distinction trips people up constantly — a directory can be world-readable but still inaccessible if the execute bit isn't set.

### 12. `12-directory_permissions` — done the job
**Command used:** `chmod -R` (recursive)

```bash
chmod -R u+x my_dir
```
The `-R` flag applies the permission change **recursively**, to the directory and everything inside it. This is what you actually reach for in practice — changing permissions on a single top-level directory almost never matters if the files inside still have the old permissions.

### 13. `13-change_group` — done the job
**Command used:** `chgrp`

```bash
chgrp school my_file
```
`chgrp` changes a file's **group** ownership specifically, without touching the user owner. It's the group-focused counterpart to `chown`, useful when several users share group-level access to a resource (e.g. a shared project directory).

### 100. `100-change_owner_and_group` — done the job
**Command used:** `chown` (owner and group together)

```bash
chown busta_rhymes:root my_file
```
`chown` can set **both** owner and group in a single command using `owner:group` syntax, instead of calling `chown` and `chgrp` separately. This is the syntax you'll actually see in real deployment scripts and Dockerfiles.

### 101. `101-symbolic_link_permissions` — done the job
**Command used:** `chmod -h` (or equivalent, on a symlink)

```bash
chmod -h 754 my_symbolic_link
```
Permissions on a **symbolic link** are a special case: changing a symlink's permissions normally changes the permissions of the file it *points to*, not the link itself, because most systems ignore a symlink's own permission bits. The `-h` flag tells `chmod` to affect the link, not its target — an important distinction when scripting around linked config files (e.g. `/etc/nginx/sites-enabled/`).

### 102. `102-if_only` — done the job
**Command used:** conditional permission logic (`test`/`[ ]` combined with `chmod`)

```bash
if [ -g my_file ]; then
    chmod u+x my_file
fi
```
Combines a permission **test** (checking a specific bit, like the setgid flag with `-g`) with a conditional `chmod` action. This is the first real fusion of the permissions module with the conditional logic from `0x04-loops_conditions_and_parsing` — real administration scripts rarely apply a change unconditionally; they check the current state first.

### 103. `103-Star_Wars` — done the job
**Command used:** advanced/bonus permissions task

This is the module's bonus challenge, combining several of the concepts above (ownership, numeric/symbolic modes, and conditional checks) into a single more elaborate script. I'm intentionally not overstating its exact internals here without re-reading the script itself — but structurally it reinforces the same core skill as the rest of the module: predicting and controlling exactly who can read, write, or execute a given resource.

---

## Skills Demonstrated in This Module

- **Identity on a Unix system**: `whoami`, `groups`, `su` — knowing who you are and what you belong to before you act
- **Ownership control**: `chown`, `chgrp`, and the combined `owner:group` syntax
- **Permission syntax fluency**: both symbolic (`u+x`, `g-w`, `o=r`) and numeric (`755`, `007`, `700`) modes, and translating fluently between the two
- **Recursive operations**: `chmod -R` for directories and their contents
- **Edge cases that matter in production**: symlink permissions (`-h`), directory execute bits meaning "enter," and permission inheritance via `--reference`
- **Conditional logic applied to system state**: checking a permission bit before acting on it, instead of blindly overwriting

## Why This Matters Beyond the Exercises

Almost every real-world security hardening task — locking down an SSH key, restricting a config file so only a service account can read it, making sure a shared directory is writable by a team but not the world — is just a more consequential version of these exercises. This module is where "permissions" stopped being an abstract concept from a textbook and became something I can read off a terminal (`-rwxr-xr--`) and immediately understand.

## Requirements

- Ubuntu 16.04/20.04 LTS
- Bash scripts, tested with multiple users/groups where relevant (e.g. `betty`)

## Author

**SwissKnifeTech** — ALX System Engineering & DevOps track
