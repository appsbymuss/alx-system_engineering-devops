# 0x04. Loops, Conditions & Parsing

This module is where shell scripting stops being "a sequence of commands" and starts being **actual programming**: repetition (loops), decision-making (conditionals), and reading structured input (parsing). Every script before this one ran top to bottom, once. Every script here makes a decision about *what* to run, or runs something *more than once* — which is the difference between a one-off command and a real, reusable tool.

I'm including a small honest note in the commit history itself here: several of these projects were done while my laptop was broken, worked around with whatever access I could get. I'm leaving that context in because it's true, and because finishing a module under a real constraint is arguably a better signal than a spotless commit log.

## The Core Concepts

**Loops** — `for`, `while`, and `until` all repeat a block of commands, but for different reasons: `for` iterates over a known list, `while` repeats *as long as* a condition is true, and `until` repeats *until* a condition becomes true (i.e. the inverse of `while`). Knowing which one to reach for is a readability decision as much as a functional one.

**Conditionals** — `if`/`elif`/`else` and `case` let a script branch based on a test's result. In Bash, `[ condition ]` (or `test condition`) isn't special syntax — it's actually a command that exits with status `0` (true) or non-zero (false), and `if` just checks that exit status. Understanding that "if" in Bash means "if the exit code was zero" — not "if this expression is true" in an abstract sense — is one of those small realizations that makes everything else about shell logic click.

**Parsing** — reading structured or semi-structured data (a file, command output, user input) and extracting the parts you need, usually by combining a loop with the text tools from `0x02`/`0x03`.

---

## Task-by-Task Breakdown

### 0. `0-RSA_public_key` — SSH key generation
**Command used:** `ssh-keygen`

```bash
ssh-keygen -q -f 0-RSA_public_key -t rsa -b 4096 -N ""
```
Generates a new SSH keypair non-interactively: `-t rsa -b 4096` sets the algorithm and key strength, `-f` sets the output filename, and `-N ""` sets an **empty passphrase** so the script can run without a human typing anything in. The `.pub` file in this directory is the actual output of running that script — the public half of the keypair, safe to share, as opposed to the private key which never should be. This task is a direct preview of the `0x0B-ssh` module — you can't manage remote servers securely without understanding key-based auth first.

### 1. `1-for_best_school` — done
**Command used:** `for`

```bash
for i in {0..9}; do
    echo "$i"
done
```
A `for` loop iterating over a fixed, known range (brace expansion from `0x03`, reused here as the loop's list). This is the loop you reach for when you know in advance *what* you're iterating over — a range, a list of files, an array.

### 2. `2-while_best_school` — done
**Command used:** `while`

```bash
i=0
while [ "$i" -le 9 ]; do
    echo "$i"
    i=$((i + 1))
done
```
Same output as task 1, but with `while`: repeat *as long as* the condition (`i <= 9`) holds. Unlike `for`, nothing here is known in advance — the loop manages its own counter and decides when to stop. This is the loop you use when the number of iterations depends on runtime conditions, not a fixed list.

### 3. `3-until_best_school` — done
**Command used:** `until`

```bash
i=0
until [ "$i" -gt 9 ]; do
    echo "$i"
    i=$((i + 1))
done
```
The mirror image of `while` — repeat *until* the condition becomes true, rather than *while* it's true. Functionally interchangeable with `while` if you flip the condition, but choosing the one that reads more naturally for the situation ("keep going until this becomes true") is a genuine readability skill.

### 4. `4-if_9_say_hi` — done
**Command used:** `if`

```bash
for i in {0..14}; do
    if [ "$i" -eq 9 ]; then
        echo "Best School"
    else
        echo "$i"
    fi
done
```
Introduces conditional branching inside a loop: for every number, check a condition and choose which output to produce. This is the first task where the loop's output isn't purely mechanical — it depends on a decision made each iteration.

### 5. `5-4_bad_luck_8_is_your_chance` — done
**Commands used:** `continue` and `break`

```bash
for i in {0..9}; do
    if [ "$i" -eq 4 ]; then
        continue
    elif [ "$i" -eq 8 ]; then
        break
    fi
    echo "$i"
done
```
Introduces loop **control flow**: `continue` skips the rest of the current iteration and moves to the next one (so `4` never gets printed), while `break` exits the loop entirely (so nothing after `8` runs, including `8` itself). The distinction between "skip this one" and "stop entirely" is a common source of logic bugs if you mix them up.

### 6. `6-superstitious_numbers` — done
**Command used:** `case`

```bash
for i in {0..9}; do
    case "$i" in
        4) echo "chicken";;
        8) echo "heart";;
        *) echo "$i";;
    esac
done
```
`case` is a cleaner alternative to a long `if/elif/elif/else` chain when you're comparing **one value against several fixed possibilities**. The `*)` pattern acts as the default/catch-all, similar to `else`. Readability matters here: once you have three or more discrete cases to check, `case` communicates intent more clearly than nested `if`s.

### 7. `7-clock` — done (bonus)
**Concept:** combining a loop with the `date` command

A live-updating clock built from a loop that repeatedly calls `date` (to get the current time), formats it, and re-prints it — typically with a short `sleep` between iterations. It's a fun bonus task, but the underlying pattern (poll something, format it, wait, repeat) is exactly how simple monitoring or status-display scripts work in practice.

### 8. `8-for_ls` — done
**Command used:** `for` iterating over command output

```bash
for i in $(ls); do
    echo "$i"
done
```
Loops over the output of another command rather than a fixed range — combining `for` with command substitution (`$(...)`, from `0x02`). Worth knowing the caveat: this specific pattern breaks on filenames containing spaces, since word-splitting happens on whitespace by default. It's a common beginner pattern precisely *because* it looks fine until it meets an edge case — a good lesson in testing scripts against messy real-world input, not just clean examples.

### 9. `9-to_file_or_not_to_file` — done
**Command used:** `if [ -f ]`

```bash
if [ -f "$1" ]; then
    echo "OK"
else
    echo "Not OK"
fi
```
`-f` is a **file test operator** — it checks whether a given path exists *and* is a regular file (not a directory, not a symlink to nowhere). Test operators like `-f`, `-d`, `-x`, `-e` are how scripts make decisions based on the actual state of the filesystem, not just variable values — essential for any script that needs to behave safely regardless of what it finds when it runs.

### 10. `10-fizzbuzz` — done
**Commands used:** `for`, `if`/`elif`/`else`, modulo arithmetic

```bash
for i in $(seq 1 100); do
    if [ $((i % 15)) -eq 0 ]; then
        echo -n "FizzBuzz "
    elif [ $((i % 3)) -eq 0 ]; then
        echo -n "Fizz "
    elif [ $((i % 5)) -eq 0 ]; then
        echo -n "Buzz "
    else
        echo -n "$i "
    fi
done
```
The classic FizzBuzz problem, implemented in shell. It's a well-known interview exercise for a reason: it forces correct use of the modulo operator (`%`, via `$(( ))`) and correct **ordering** of conditions — checking divisibility by 15 first is not optional, since 15 is also divisible by 3 and 5, and `elif` stops at the first true branch.

### 100. `100-read_and_cut` — done (bonus)
**Commands used:** `read` combined with parsing tools (`cut`, etc.)

```bash
while read -r line; do
    echo "$line" | cut -d: -f1
done < /etc/passwd
```
Uses `read` to pull a file in **line by line** inside a `while` loop — the standard, safe pattern for processing a file's contents one line at a time in Bash, as opposed to loading the whole thing at once. Combined with `cut` (from `0x02`) to extract a specific field from each line, this is a realistic, small-scale version of parsing a structured data file like `/etc/passwd` or a CSV export.

---

## Skills Demonstrated in This Module

- **Loop selection**: knowing when to use `for` (known list), `while` (condition-driven), or `until` (inverse condition)
- **Conditional logic**: `if`/`elif`/`else`, `case` for multi-way branching, and understanding that Bash conditionals are really just exit-code checks
- **Loop control flow**: `continue` vs. `break`, and the difference between skipping an iteration and exiting entirely
- **File and path testing**: `-f`, and the broader family of test operators used to make a script filesystem-aware
- **Line-by-line file processing**: the `while read -r line; do ... done < file` pattern, safer than looping over `cat` output
- **Non-interactive key generation**: `ssh-keygen` with explicit flags, in preparation for real SSH-based remote administration

## Why This Matters Beyond the Exercises

Almost every real automation script — a deployment script, a backup script, a log-rotation job — is fundamentally "loop over some things, and for each one, decide what to do based on its current state." This module is where I built the actual control-flow vocabulary that every later, more complex script in this repository (configuration management, monitoring, debugging) depends on.

## Requirements

- Ubuntu 16.04/20.04 LTS
- Bash
- `ssh-keygen` available (part of OpenSSH client tools)

## Author

**SwissKnifeTech** — ALX System Engineering & DevOps track
