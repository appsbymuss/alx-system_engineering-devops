# 0x02. Shell Redirections
 
This module is about a single, powerful idea in Unix: **every program reads from somewhere and writes to somewhere, and you can rewire both.** Once you understand that a command doesn't inherently "print to the screen" — it writes to a file descriptor that *happens* to point at your terminal by default — a huge amount of shell scripting stops feeling like memorized syntax and starts feeling like plumbing you're in control of.
 
This is also the module where I started **combining** commands instead of just running them one at a time — piping the output of one into the input of another. That habit (small, composable tools chained together) is the actual philosophy behind Unix, and it's the reason a lot of DevOps automation is still built on shell pipelines instead of custom programs.
 
## The Core Concept: File Descriptors & Streams
 
Every process starts with three open streams:
 
| Descriptor | Name | Default destination |
|---|---|---|
| `0` | **stdin** (standard input) | your keyboard |
| `1` | **stdout** (standard output) | your terminal screen |
| `2` | **stderr** (standard error) | your terminal screen |
 
Redirection operators let you point these somewhere else:
 
| Operator | Meaning |
|---|---|
| `>` | Redirect stdout to a file, **overwriting** it |
| `>>` | Redirect stdout to a file, **appending** to it |
| `<` | Feed a file in as stdin |
| `2>` | Redirect stderr specifically |
| `2>&1` | Redirect stderr to wherever stdout is currently going |
| `\|` | Pipe — send one command's stdout directly into another command's stdin |
 
Almost every task in this module is a variation on one of these operators, or a pipeline built from several commands chained with `|`.
 
---
 
## Task-by-Task Breakdown
 
### 0. `0-hello_world` — Hello World
**Concept:** stdout vs. stderr
 
```bash
echo "Hello, World" 2>/dev/null
```
Prints "Hello, World" to stdout, while explicitly sending stderr to `/dev/null` (a special file that discards anything written to it). Even though this particular command doesn't produce an error, the point of the exercise is proving the message survives *even if stderr is being thrown away* — proof that stdout and stderr really are two independent streams.
 
### 1. `1-confused_smiley` — Confused smiley
**Concept:** fixing broken syntax, careful use of `echo`/quoting
 
Fixes a script whose smiley face was written backwards (e.g. `(-:` instead of `:-)`), reinforcing how easily a single misplaced character breaks a script's output — and that debugging often starts with reading output character by character.
 
### 2. `2-hellofile` — Let's display a file
**Command used:** `cat`
 
```bash
cat /etc/passwd
```
`cat` (concatenate) prints a file's contents to stdout. It's the simplest possible way to read a file from the shell, and the building block for the redirection tasks that follow.
 
### 3. `3-twofiles` — done
**Command used:** `cat` with multiple files
 
```bash
cat /etc/passwd /etc/hosts
```
`cat` can take multiple filenames and prints them back-to-back, as if they were one file. This is genuinely how log files get combined for quick inspection during debugging.
 
### 4. `4-lastlines` — done
**Command used:** `tail`
 
```bash
tail -n 10 /etc/passwd
```
Prints the **last** 10 lines of a file. In real operations, `tail` (often with `-f` to "follow" a growing file) is one of the most-used commands there is — it's how you watch a log file update in real time during an incident.
 
### 5. `5-firstlines` — done
**Command used:** `head`, with input redirection
 
```bash
head -n 10 < /etc/passwd
```
Prints the **first** 10 lines. Using `<` to feed the file in as stdin (rather than passing it as an argument) is a deliberate exercise in the input-redirection operator — functionally similar here, but it proves you understand `<` is a different mechanism than "pass a filename argument."
 
### 6. `6-third_line` — done
**Commands used:** `head` piped into `tail`
 
```bash
head -n 3 /etc/passwd | tail -n 1
```
Combines two commands to isolate a single, specific line: take the first 3 lines, then take the last 1 of *those*. This is the first real "pipeline" in the module — solving a problem neither command could solve alone.
 
### 7. `7-file` — done
**Commands used:** `ls`, `sort`, `file`, piped together
 
```bash
file "$(ls -S | head -n 1)"
```
Finds the largest file in the current directory (`ls -S` sorts by size, largest first) and passes it to `file` to identify its type. This is a good example of **command substitution** (`$(...)`) — using one command's output as another command's *argument*, which is subtly different from piping it as *input*.
 
### 8. `8-cwd_state` — done
**Command used:** `ls` redirected to two files
 
```bash
ls -la > .cwd_state
ls -l > cwd_state
```
Captures a snapshot of the current directory's contents into files — one including hidden files, one not. This is essentially a manual, tiny version of what configuration-drift or audit tooling does: record the state of something now, so you can diff it against a later state.
 
### 9. `9-duplicate_last_line` — done
**Command used:** `tail` appended back into the same file
 
```bash
tail -n 1 iyaach >> iyaach
```
Reads the last line of a file and appends (`>>`) a copy of it to the end of the same file. A small but important lesson: `>>` never destroys existing content the way `>` would — which is exactly why you use it here instead of `>`, which would have wiped the whole file down to just that one line.
 
### 10. `10-no_more_js` — done
**Command used:** `find` with deletion
 
```bash
find . -name "*.js" -not -path "./node_modules/*" -delete
```
`find` searches recursively for files matching a pattern and deletes them directly with `-delete` — no need to pipe into `rm`. Excluding `node_modules` is a very real, very common pattern: you almost never want to touch dependency directories when cleaning up a project.
 
### 11. `11-directories` — done
**Commands used:** `ls -l` piped into `grep`
 
```bash
ls -l | grep "^d"
```
Filters a long-format listing down to only lines starting with `d` — the character `ls -l` uses to mark a directory. This is a very common trick: rather than a dedicated flag, you filter `ls`'s own output with `grep`.
 
### 12. `12-newest_files` — done
**Command used:** `ls -t`
 
```bash
ls -t | head -n 10
```
`-t` sorts by modification time, newest first. Paired with `head`, this answers a question you'll ask constantly on a real server: "what changed most recently?"
 
### 13. `13-unique` — done
**Command used:** `sort -u`
 
```bash
sort -u file
```
Sorts a file's lines and removes duplicates in one pass. `sort` and `uniq` are often used together (`sort file | uniq`), but `-u` does both jobs at once — a nice shortcut once you understand `sort` well enough to know the flag exists.
 
### 14. `14-findthatword` — done
**Command used:** `grep`
 
```bash
grep "root" /etc/passwd | wc -l
```
`grep` searches for lines matching a pattern; piping the matches into `wc -l` (word count, line mode) turns "which lines match" into "how many lines match." This exact pattern — `grep | wc -l` — is one of the most common one-liners in real system administration.
 
### 15. `15-countthatword` — done
**Command used:** `grep -o` (only the match, not the whole line)
 
```bash
grep -o -i "Bytes" aBigFile | wc -l
```
`-o` prints only the matched text itself, not the surrounding line — which matters when counting **occurrences** of a word rather than lines that merely contain it (a line could contain the word twice). `-i` makes the match case-insensitive.
 
### 16. `16-whatsnext` — done
**Command used:** `grep -A`
 
```bash
grep -A 1 "root" /etc/passwd
```
`-A 1` prints the matching line **plus the line immediately after it** (After-context). Useful when the line you actually care about is identified *relative to* a pattern, rather than by a pattern of its own.
 
### 17. `17-hidethisword` — done
**Command used:** `grep -v`
 
```bash
grep -v "root" /etc/passwd
```
`-v` inverts the match — prints every line that does **not** contain the pattern. This is the "everything except" filter, used constantly to strip out noise from logs.
 
### 18. `18-letteronly` — done (with a fix commit — the messy, real part of learning)
**Command used:** `grep` with a regex anchor
 
```bash
grep -E "^[a-zA-Z]" /etc/passwd
```
Matches only lines that **start** with a letter, using the `^` anchor. Worth calling out: the commit history here literally shows me fixing this task after an initial attempt — regex anchors and character classes are exactly the kind of thing that looks simple and isn't, until you've debugged a wrong result once.
 
### 19. `19-AZ` — done
**Command used:** `tr`
 
```bash
tr 'a-z' 'A-Z' | tr 'A' '_'
```
`tr` (translate) maps one set of characters to another, character-by-character, across a whole stream — not line-by-line like `grep`/`sed`. Chaining two `tr` calls (uppercase everything, then replace one specific letter) shows how narrowly-scoped Unix tools compose into more complex transformations.
 
### 20. `20-hiago` — done
**Command used:** `sed`
 
```bash
sed 's/Ago/Hi/g'
```
Uses `sed`'s substitute command again (seen first in `0x00`), this time as a real find-and-replace across a stream — a pattern used everywhere from config templating to log redaction.
 
### 21. `21-reverse` — done
**Command used:** `rev`
 
```bash
rev
```
Reverses the characters of each line of input. A small utility, but a good reminder that Unix has a *lot* of narrowly single-purpose tools — knowing `rev` exists saves you from writing a manual character-reversal loop.
 
### 22. `22-users_and_homes` — done
**Commands used:** `cut` and `sort`
 
```bash
cat /etc/passwd | cut -d: -f1,6 | sort
```
`cut` extracts specific **fields** from structured text using a delimiter (`:` in `/etc/passwd`) — here, the username (field 1) and home directory (field 6) — then `sort` orders the result. This is exactly how you'd audit "who has access to this system and where does their home directory live" from the command line.
 
### 100. `100-empty_casks` — done
**Command used:** `find -empty`
 
```bash
find . -empty -type f -delete
```
Finds and deletes every **empty file** in the current directory tree. `find`'s `-empty` test is a good example of how much logic `find` can express on its own, without piping into other commands at all.
 
### 101. `101-gifs` — done
**Command used:** `find`, filtered and sorted
 
```bash
find . -maxdepth 1 -name "*.gif" -type f | sort
```
Finds files by extension and sorts the result — a pattern used constantly for asset audits (e.g. "list every image in this directory before a deploy").
 
### 102. `102-acrostic` — done
**Commands used:** `cut` or a loop, extracting the first character per line
 
```bash
cut -c1 story
```
Reads a text file and extracts just the **first character of each line** — turning a block of text into an acrostic. It's a playful task, but `cut -c` (character-position extraction) is genuinely useful for fixed-width data formats, which still show up in legacy systems and some log formats.
 
### 103. `103-the_biggest_fan` — done (bonus)
**Commands used:** a full pipeline: `tr`, `sort`, `uniq -c`, `sort -nr`, `head`
 
```bash
tr -s ' ' '\n' < file | sort | uniq -c | sort -nr | head -n 10
```
The capstone pipeline of the module: split text into one word per line, sort so identical words are adjacent, count consecutive duplicates with `uniq -c`, sort numerically descending, and take the top results. This exact pipeline (`tr | sort | uniq -c | sort -nr`) is a genuine, widely-used pattern for **word-frequency analysis** — the same idea scales to counting log error types, counting HTTP status codes in access logs, or counting IPs hitting an endpoint.
 
---
 
## Skills Demonstrated in This Module
 
- **Stream redirection**: `>`, `>>`, `<`, `2>` and the distinction between stdout and stderr
- **Pipelines**: chaining commands with `|` to solve problems no single command handles alone
- **Text filtering**: `grep` (`-v`, `-A`, `-o`, `-i`, regex anchors like `^`)
- **Text transformation**: `sed` substitution, `tr` character translation, `cut` field/character extraction
- **Sorting and deduplication**: `sort`, `sort -u`, `sort -t`, `uniq -c`
- **File discovery and cleanup**: `find` with `-name`, `-empty`, `-delete`, `-not -path`
- **Command substitution**: using `$(...)` to feed one command's output into another as an argument
## Why This Matters Beyond the Exercises
 
Log analysis, quick audits, cleanup scripts, and one-off data extraction on a live server are almost always done with exactly these tools chained together — not custom-written programs. Being fast and precise with redirection and pipelines is a genuinely daily skill in DevOps and SRE work, and it's usually the first thing that separates "comfortable in a terminal" from "reaching for a script every time."
 
## Requirements
 
- Ubuntu 16.04/20.04 LTS
- Bash, POSIX-compatible utilities (`grep`, `sed`, `tr`, `cut`, `find`, `sort`, `uniq`)
## Author
 
**SwissKnifeTech** — ALX System Engineering & DevOps track
