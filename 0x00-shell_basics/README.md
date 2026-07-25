# 0x00. Shell Basics

This is the first module of my **System Engineering & DevOps** track at ALX. Every task here is a tiny, one-line (or few-line) Bash script — but each one forces you to understand a specific Unix command well enough to use it correctly, not just copy-paste it.

I'm documenting the syntax and reasoning behind each script below, the way I'd want a teammate (or a recruiter evaluating my fundamentals) to be able to follow. The goal of this module isn't the scripts themselves — it's building the muscle memory of "what is the shell actually doing when I type this," which is the foundation everything later in the track (SSH, Puppet, load balancers, debugging) depends on.

## Why This Module Matters

Every server you'll ever touch — bare metal, VM, container, cloud instance — is operated through a shell at some point, even if 99% of your day-to-day is GUIs and dashboards. If you can't confidently navigate a filesystem, manage permissions, and manipulate files from the command line, you can't administer a system, debug it under pressure, or write automation for it. This module is where that confidence starts.

---

## Task-by-Task Breakdown

### 0. `0-current_working_directory` — Where am I?
**Command used:** `pwd`

```bash
pwd
```
`pwd` (print working directory) prints the absolute path of the directory the shell is currently "in." This is the very first thing you check when you land on an unfamiliar server via SSH — you need to know your location before you do anything else.

### 1. `1-listit` — What's in there?
**Command used:** `ls`

```bash
ls
```
Lists the contents of the current directory. No flags, no arguments — the simplest possible way to see what you're working with.

### 2. `2-bring_me_home` — There is no place like home
**Command used:** `cd`

```bash
cd
```
Running `cd` with **no argument** returns you to your home directory (`$HOME`). It's easy to assume `cd` always needs a path — knowing its no-argument default is a small but common shortcut used constantly in real sessions.

### 3. `3-listfiles` — The long format
**Command used:** `ls -l`

```bash
ls -l
```
The `-l` flag switches to **long format**, showing permissions, number of hard links, owner, group, file size, and last-modified timestamp for every entry. This is the listing format you actually use when you need information, not just names — e.g. checking if a file is executable, or who owns it.

### 4. `4-listmorefiles` — Hidden files
**Command used:** `ls -la`

```bash
ls -la
```
Adding `-a` (all) includes **hidden files** — anything starting with a `.`, like `.bashrc` or `.ssh`. In Unix, "hidden" just means "filtered out of the default listing," not actually protected. Config files almost always live in dotfiles, so `-a` is essential when troubleshooting environment or shell configuration issues.

### 5. `5-listfilesdigitonly` — I love numbers
**Command used:** `ls -la` piped or combined with `-n`

```bash
ls -na
```
The `-n` flag is like `-l`, but shows the **numeric** user ID (UID) and group ID (GID) instead of resolving them to names. This matters when a system's `/etc/passwd` doesn't have a name mapped to a UID (common when copying files between servers, or in containers) — you still need to identify ownership by number.

### 6. `6-firstdirectory` — Welcome
**Command used:** `mkdir`

```bash
mkdir my_first_directory
```
Creates a new, empty directory. `mkdir` is the starting point for any structured file organization — and later, for staging deployment directories, log directories, or config directories on a server.

### 7. `7-movethatfile` — Betty in my first directory
**Command used:** `mv`

```bash
mv betty my_first_directory
```
`mv` moves (or renames) a file. Unix doesn't have a separate "rename" command — moving a file to a new name *in the same directory* is how renaming works, which trips up a lot of beginners coming from GUI file managers.

### 8. `8-firstdelete` — Bye bye Betty
**Command used:** `rm`

```bash
rm ./my_first_directory/betty
```
Deletes a file. There's no "trash" or "recycle bin" in the shell by default — `rm` is permanent. This task is small, but it's the first real lesson in the *seriousness* of shell commands: a typo in a path here can mean data loss on a real system.

### 9. `9-firstdirdeletion` — Bye bye My first directory
**Command used:** `rmdir`

```bash
rmdir my_first_directory
```
`rmdir` removes a directory, but **only if it's empty**. That constraint is a safety feature — it stops you from silently deleting a directory (and everything in it) with one command. To delete a non-empty directory you'd need `rm -r`, which is intentionally a bigger, more deliberate command.

### 10. `10-back` — Back to the future
**Command used:** `cd ..`

```bash
cd ..
```
Moves one level up in the directory tree. `.` refers to the current directory, `..` to its parent — this two-character convention is used everywhere in Unix paths, including in relative script references (`./script.sh`).

### 11. `11-lists` — Lists
**Command used:** file creation

```bash
touch hello
```
Creates a file named `hello`. Simple as it looks, `touch` is what you reach for constantly — to create empty placeholder files, or to update a file's modification timestamp without changing its content (useful for triggering file-watchers or build systems).

### 12. `12-file_type` — File type: School
**Command used:** `file`

```bash
file school.mgc
```
`file` inspects a file's actual content (its "magic bytes") to determine its type — regardless of its extension. This task pairs with the custom `school.mgc` magic file included in this directory, which teaches the `file` command to recognize a custom, made-up file type. This is a good example of *why* Unix tools are configurable: `file` doesn't guess from the filename, it reads real byte signatures, and you can extend what it recognizes.

### 13. `13-symbolic_link` — We are symbols, and inhabit symbols
**Command used:** `ln -s`

```bash
ln -s /etc/amazing /tmp/school
```
Creates a **symbolic link** — a pointer file that redirects to another path. This is heavily used in real deployments: e.g. pointing `/etc/nginx/sites-enabled/site` to a config in `/etc/nginx/sites-available/`, or keeping a `current` symlink pointing at whichever release directory is live, so a deploy is just "repoint the symlink."

### 14. `14-copy_html` — Copy HTML files
**Command used:** `cp`

```bash
cp -R -v ./web_static ~/my_html
```
Copies files/directories, with `-R` for **recursive** (needed for directories) and `-v` for **verbose** output (prints each file as it's copied). This task specifically involves filenames containing spaces, which is a classic Unix gotcha — it forces you to think about quoting and escaping (`"file name.html"` vs `file\ name.html`), a habit that prevents silent script failures later.

### 100. `100-lets_move` — Let's move
**Command used:** `mv` with a wildcard/glob

```bash
mv [0-9]* numbers/
```
Moves every file whose name **starts with a digit** into a `numbers` directory, using a bracket-expression glob (`[0-9]*`) rather than a literal filename. This is the first real taste of pattern matching in the shell — a precursor to the regular expressions used later in the track.

### 101. `101-clean_emacs` — Clean Emacs
**Command used:** `rm`

```bash
rm -f *~
```
Deletes Emacs backup files, which are automatically named with a trailing `~` (e.g. `notes.txt~`). Real systems accumulate this kind of editor/tool debris constantly — knowing how to safely clean up generated cruft (without deleting real files) is a genuinely practical sysadmin habit.

### 102. `102-tree` — Tree
**Command used:** `find -type d`

```bash
find . -type d | wc -l
```
Counts every **directory** under the current path. `find` is far more powerful than `ls` for this — it recurses automatically and can filter by type, name, age, size, and more. `-type d` restricts results to directories only, and piping into `wc -l` turns a list into a count. This combination (`find | wc -l`) is an extremely common pattern for auditing a filesystem.

### 103. `103-commas` — Life is a series of commas, not periods
**Command used:** `sed`

```bash
sed 's/\./,/g'
```
Uses `sed` (stream editor) to substitute every period with a comma. `s/pattern/replacement/g` is the core syntax of `sed`'s substitute command — `s` for substitute, and the trailing `g` for **global** (replace every match on a line, not just the first). This is a first, small step toward the regular-expressions module later in the track, where `sed` is used for real text-processing tasks like log parsing and config templating.

---

## Skills Demonstrated in This Module

- **Filesystem navigation**: `pwd`, `cd`, `cd ..`, relative vs. absolute paths
- **Inspecting files and directories**: `ls` and its flags (`-l`, `-a`, `-n`), `file`
- **File and directory manipulation**: `mkdir`, `rmdir`, `mv`, `rm`, `cp`, `touch`
- **Links**: symbolic links with `ln -s` and why they're used in deployments
- **Pattern matching**: glob expressions (`[0-9]*`, `*~`) and an early introduction to `sed` substitution
- **Search and filtering**: `find` combined with `wc -l` for filesystem audits
- **Attention to edge cases**: filenames with spaces, hidden files, empty vs. non-empty directories

Every one of these is a command I still use daily when SSH'd into a server — this module is where they stopped being "commands I looked up" and became "commands I reach for without thinking."

## Requirements

- Ubuntu 16.04/20.04 LTS
- All scripts are Bash, no more than a few lines
- Scripts are meant to be read and understood in seconds — the constraint of "keep it minimal" is intentional, to force precision over cleverness

## Author

**SwissKnifeTech** — ALX System Engineering & DevOps track
