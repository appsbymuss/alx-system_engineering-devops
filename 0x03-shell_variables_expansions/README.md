# 0x03. Shell Variables & Expansions

Where `0x02` was about rewiring *streams*, this module is about rewiring *values*. It covers three related ideas that, together, are the difference between a script that just runs commands in sequence and a script that actually **computes** and **reasons**: variables (storing state), environment variables (sharing state with other programs), and shell arithmetic/expansion (doing math and string manipulation without leaving Bash).

This is also where I stopped thinking of the shell as "just a way to run programs" and started treating it as a real, if quirky, programming environment — with scope, arithmetic, and its own expansion rules.

## The Core Concepts

**Local vs. global (environment) variables** — a variable set with `VAR=value` only exists in the current shell. Prefixing it with `export` promotes it to an **environment variable**, which means any child process spawned from that shell inherits a copy of it. This distinction matters constantly: it's why setting `PATH` in one terminal doesn't affect another, and why forgetting `export` is a classic source of "why can't my script see this variable" bugs.

**`$` expansion** — `$VARNAME` (or `${VARNAME}`) tells the shell "replace this with the variable's value before running the command." Nearly everything in this module is really just applying that one rule in different contexts.

**Arithmetic isn't native to Bash strings** — Bash treats everything as text by default, so numeric work needs either `$(( ))` (built-in integer arithmetic) or an external tool like `bc` (arbitrary-precision calculator) for anything beyond basic integer math — including exponents, division with decimals, or base conversion.

---

## Task-by-Task Breakdown

### 0. `0-alias` — done
**Command used:** `alias`

```bash
alias ls="rm *"
```
Creates a shortcut name (`ls`) that actually runs a *different*, dangerous command (`rm *`). It looks like a joke, but it's a genuinely important security lesson: aliases silently override commands you trust, which is exactly the kind of thing a malicious `.bashrc` could exploit. Always know what an alias actually expands to before trusting it.

### 1. `1-hello_you` — done
**Command used:** variable expansion with `$USER`

```bash
echo "hello $USER"
```
`$USER` is an environment variable set by the system, holding the current username. This is the simplest possible demonstration of expansion: the shell substitutes the variable's value into the string *before* `echo` ever sees it.

### 2. `2-path` — done
**Command used:** modifying `$PATH`

```bash
export PATH="$PATH:/root/bin"
```
`$PATH` is the list of directories the shell searches, in order, when you type a command name. Appending to it (rather than overwriting it) is critical — `PATH="/root/bin"` alone would break every other command on the system. This is the real-world way custom scripts and installed tools become runnable by name instead of needing a full path every time.

### 3. `3-paths` — done
**Commands used:** `tr` and `wc`, applied to `$PATH`

```bash
echo -n "$PATH" | tr ":" "\n" | sort -u | wc -l
```
Counts how many directories are listed in `$PATH` by turning the colon-separated string into one line per directory, then counting lines. A nice example of applying the text-processing tools from `0x02` to a *variable's value* instead of a file.

### 4. `4-global_variables` — done
**Command used:** `env` (or `printenv`)

```bash
env
```
Lists every environment variable available to the current process. Genuinely one of the first commands I'd run when debugging "why does this script behave differently on this server than on mine" — differences in environment variables are a very common cause.

### 5. `5-local_variables` — done
**Command used:** `set`

```bash
set
```
Lists **all** variables visible to the current shell — local variables, environment variables, and even defined functions — unlike `env`, which only shows exported ones. Comparing the output of `set` and `env` side-by-side is actually the clearest way to *see* the local-vs-global distinction instead of just reading about it.

### 6. `6-create_local_variable` — done
**Syntax:** direct assignment

```bash
BEST="School"
```
No spaces around `=` — that's not a style preference, it's required syntax; `BEST = "School"` is actually parsed as *running a command called `BEST`* with two arguments. This variable exists only in the current shell session.

### 7. `7-create_global_variable` — done
**Command used:** `export`

```bash
export BEST="School"
```
Same idea as task 6, but `export` promotes it to the environment, meaning any script or subprocess launched from this shell inherits a copy of `BEST`. This is the exact mechanism configuration values get passed into applications in real deployments (e.g. `export DATABASE_URL=...` before starting a service).

### 8. `8-true_knowledge` — done
**Command used:** arithmetic expansion `$(( ))`

```bash
echo $((128 + 73))
```
Bash's built-in arithmetic expansion evaluates integer math directly, no external tool required. Fast, but limited — it only handles integers, which is exactly the limitation the next two tasks work around.

### 9. `9-divide_and_rule` — done
**Command used:** `bc`

```bash
echo "291 / 98" | bc
```
`$(( ))` can't produce decimal results — division truncates to an integer. `bc` (basic calculator) reads an expression from stdin and can. Piping a math expression into `bc` is the standard way to get real precision out of a shell script.

### 10. `10-love_exponent_breath` — done
**Command used:** `bc`

```bash
echo "89 ^ 2" | bc
```
Same tool, different operator — `bc` supports exponentiation (`^`) natively, which `$(( ))` in plain Bash does not (without Bash-specific extensions). Knowing when to reach for `bc` versus native arithmetic is a genuinely practical judgment call.

### 11. `11-binary_to_decimal` — done
**Command used:** `bc` with base conversion

```bash
echo "ibase=2; 110011001" | bc
```
`bc` supports setting the **input base** (`ibase`) before evaluating an expression — here, telling it to interpret the following number as binary. Base conversion shows up in real infrastructure work more than people expect: subnet masks, permission bits, and color codes are all just numbers in a different base.

### 12. `12-combinations` — fix commit included
**Concept:** brace expansion and loops

```bash
for i in {a..z}; do
    for j in {a..z}; do
        [ "$i$j" != "oo" ] && echo -n "$i$j"
    done
done
```
`{a..z}` is **brace expansion** — the shell generates the full alphabet as a list, without you writing it out. This task pairs that expansion with a nested loop to generate every two-letter combination except one excluded case. Worth noting honestly: the commit history shows a fix here — getting the exclusion and the output formatting exactly right (no trailing separator, no extra newline) is a good example of how "almost correct" shell output is still wrong output.

### 13. `13-print_float` — done
**Command used:** `printf`

```bash
printf "%.3f\n" "$1"
```
`printf` (unlike `echo`) supports format specifiers, letting you control exactly how a number is displayed — here, forcing 3 decimal places. This is the shell-scripting equivalent of formatted string output in higher-level languages.

### 100. `100-decimal_to_hexadecimal` — done
**Command used:** `bc` with output base

```bash
echo "obase=16; $1" | bc
```
The counterpart to task 11 — `obase` sets the **output** base instead of the input base, converting a normal decimal number into hexadecimal. Hex shows up constantly in real system work: color codes, memory addresses, and file permissions (in some contexts) are all commonly represented in hex.

### 101. `101-rot13` — done
**Command used:** `tr`, character-shifted

```bash
tr 'a-zA-Z' 'n-za-mN-ZA-M'
```
Implements the ROT13 cipher — shifting every letter 13 places through the alphabet — entirely with `tr`'s character-mapping feature, no loop required. It's a fun task, but it's a genuinely good demonstration of how much `tr` can do once you think of it as "map alphabet A onto alphabet B," not just "swap case."

### 102. `102-odd` — done
**Command used:** `seq`

```bash
seq 1001 2 9999
```
`seq` generates a sequence of numbers, and its three-argument form (`start step end`) can generate only odd numbers directly, without any filtering logic needed. A good reminder to check whether a command's flags already solve your problem before reaching for a loop.

### 103. `103-water_and_stir` — done (bonus)
**Concept:** a combined bonus exercise

The module's bonus/advanced task, tying together arithmetic expansion, `bc`, and variable manipulation into a more elaborate script. As with the other bonus tasks across this repo, I'd rather point to the actual file for its exact logic than guess at specifics here — but structurally it reinforces the same core skill as the rest of the module: manipulating numeric values precisely and predictably from the shell.

---

## Skills Demonstrated in This Module

- **Variable scope**: local vs. environment (`export`) variables, and why the distinction matters for child processes
- **Expansion mechanics**: `$VAR` substitution, `{a..z}` brace expansion, command substitution
- **Shell arithmetic**: `$(( ))` for fast integer math, `bc` for decimals, exponents, and base conversion
- **Formatted output**: `printf` for precise, controlled formatting versus `echo`'s simplicity
- **Introspection**: `env`, `set`, and `$PATH` inspection as debugging tools for environment-related issues
- **Text-as-data manipulation**: applying `tr`/`wc`/`sort` (from `0x02`) to variable values, not just files

## Why This Matters Beyond the Exercises

Environment variables are how real applications receive configuration in almost every deployment context — Docker containers, systemd services, CI/CD pipelines, cloud functions. Understanding exactly when a variable is visible to a subprocess (and when it isn't) is the difference between a five-minute config fix and an hour spent confused about why a service "can't see" a value you're sure you set.

## Requirements

- Ubuntu 16.04/20.04 LTS
- Bash, `bc` (may need `apt install bc` on a fresh system)

## Author

**SwissKnifeTech** — ALX System Engineering & DevOps track
