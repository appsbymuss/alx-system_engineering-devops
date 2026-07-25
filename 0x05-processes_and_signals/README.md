# 0x05. Processes & Signals

Every command you've run in this repository so far has been a **process** — a running instance of a program, with its own process ID (PID), its own memory, and a defined lifecycle: start, run, and eventually terminate. This module is about seeing and controlling that lifecycle directly: inspecting what's running, understanding how a shell script itself is just another process, and learning **signals** — the mechanism the OS uses to tell a process "stop," "reload," or "you're being forcibly killed."

This is a module that matters every single day in real operations. "The service won't stop," "how do I gracefully restart this without dropping active connections," "why is this process a zombie and eating a PID slot" — these are all questions this module directly answers.

## The Core Concepts

**PID (Process ID)** — every running process has a unique numeric identifier assigned by the kernel. `$$` inside a shell script refers to *that script's own* PID.

**Signals** — small, standardized messages sent to a process to influence its behavior. The two you'll hear about constantly:
- `SIGTERM` (15) — "please terminate" — the *polite* request. A well-behaved program can catch this and clean up before exiting (close files, finish a request, save state).
- `SIGKILL` (9) — "terminate now" — cannot be caught, ignored, or handled. The kernel kills the process immediately, no cleanup possible.

Between those two extremes are others like `SIGHUP` (historically "the terminal hung up," now often reused to mean "reload your config") and `SIGINT` (what `Ctrl+C` actually sends).

**Zombies** — when a process finishes but its **parent** hasn't yet acknowledged its exit status, it becomes a zombie: dead, but still holding a slot in the process table until the parent "reaps" it. Understanding zombies is understanding that a process doesn't just vanish the instant it finishes — cleanup is a distinct, separate step.

---

## Task-by-Task Breakdown

### 0. `0-what-is-my-pid` — done
**Special variable used:** `$$`

```bash
echo "$$"
```
`$$` expands to the PID of the **current shell/script**, not any command it might run. This is the starting point for everything else in the module — before you can manage or signal a process, you need to be able to identify it.

### 1. `1-list_your_processes` — done
**Command used:** `ps`

```bash
ps -ef
```
`ps` (process status) lists running processes. `-e` shows every process on the system (not just ones attached to your terminal), and `-f` gives the "full" format — PID, parent PID (PPID), start time, and the full command line. This is the single most-used diagnostic command for "what's actually running on this box right now."

### 2. `2-show_your_bash_pid` — done
**Concept:** a script that reports and holds its own PID

```bash
echo "I'm process $$"
sleep infinity
```
Prints the script's own PID and then deliberately hangs, so that the process stays alive long enough to be found (via `ps`) and signaled from another terminal. This task is really a setup for the signal-handling tasks that follow — you can't practice sending signals to a process that's already finished.

### 3. `3-show_your_bash_pid_made_easy` — done
**Concept:** the same idea, simplified

A cleaner version of task 2, reinforcing that `$$` reliably refers to the running shell's own PID without needing a subshell or extra indirection — an important distinction, since `$$` and `$BASHPID` aren't always the same thing inside subshells, and it's easy to reach for the wrong one.

### 4. `4-to_infinity_and_beyond` — done
**Concept:** an intentionally endless process

```bash
while true; do
    :
done
```
A script with no natural exit condition — it runs forever until something external stops it. This exists specifically to give the next tasks something to *practice signaling*. In real systems, long-running services (web servers, daemons) are exactly this: processes designed to run indefinitely until told otherwise.

### 5. `5-dont_stop_me_now` — done
**Concept:** ignoring `SIGTERM`

```bash
trap "" SIGTERM
while true; do
    :
done
```
`trap` lets a script define custom behavior for a given signal. Trapping `SIGTERM` with an empty action means the script **ignores** the polite "please stop" request entirely and keeps running. This is a deliberately provocative exercise — it proves `SIGTERM` is a *request*, not a guarantee, and sets up the contrast with `SIGKILL` in the next task.

### 6. `6-stop_me_if_you_can` — done
**Concept:** trapping `SIGTERM` with a custom response

```bash
trap "echo 'I blocked the signal'" SIGTERM
while true; do
    :
done
```
Similar to task 5, but the trap actually *does something* — prints a message — every time `SIGTERM` arrives, then keeps running anyway. The lesson: a process can be written to respond to a termination request however it wants, including by refusing it. The only way to guarantee it stops is `kill -9` (`SIGKILL`), which the process has no ability to intercept.

### 7. `7-highlander` — done
**Concept:** single-instance enforcement ("there can be only one")

```bash
pkill -9 -f highlander
```
A script that ensures only **one** copy of itself is ever running — killing any existing instance before continuing (or refusing to start a second one). `pkill` finds and signals processes **by name/pattern** rather than requiring you to already know the PID, using `-f` to match against the full command line. This exact pattern — preventing duplicate instances — is used in real services and cron jobs to avoid two copies of a backup or sync job colliding.

### 8. `8-beheaded_process` — done
**Concept:** detaching a process from its parent shell

```bash
nohup some_command &
```
`nohup` ("no hangup") makes a process **immune to `SIGHUP`** — the signal normally sent to child processes when the terminal that launched them closes. Combined with `&` (running in the background), this is exactly how you start a long-running process from an SSH session and have it survive after you disconnect — the origin of the "beheaded" name: the process keeps running even after its "head" (the parent shell) is gone.

### 100. `100-process_and_pid_file` — done (bonus)
**Concept:** a self-daemonizing script with a PID file

```bash
echo $$ > /var/run/my_process.pid
while true; do
    sleep 1
done
```
Writes its own PID to a well-known file location before running indefinitely. This is a real, production pattern: services write a `.pid` file specifically so that **other** scripts (start/stop/restart tooling, monitoring, init systems) can find and manage them without needing to search process listings by name. It's a small task, but it's genuinely how a lot of pre-systemd service management worked, and the concept still shows up in custom tooling today.

### 102. `102-zombie.c` — done (bonus, written in C)
**Concept:** deliberately creating a zombie process

```c
#include <unistd.h>

int main(void) {
    if (fork() == 0) {
        _exit(0); /* child exits immediately */
    }
    sleep(60);   /* parent doesn't wait() — child stays a zombie */
    return 0;
}
```
Uses `fork()` to create a child process that exits immediately, while the **parent** deliberately does *not* call `wait()` to acknowledge that exit. The result is a real, observable zombie process (`ps` will show it with state `Z`) for as long as the parent keeps running without reaping it. This is the one C program in an otherwise all-Bash module, and it's included for a good reason: zombies are a kernel/process-table concept that shell alone can illustrate but not truly *cause* on demand — seeing it built at the syscall level (`fork`, `exit`, `wait`) makes the concept concrete instead of theoretical.

---

## Skills Demonstrated in This Module

- **Process identification**: `$$`, `ps -ef`, reading PID/PPID relationships
- **Signal theory and practice**: the difference between a catchable request (`SIGTERM`, `SIGHUP`) and an unstoppable command (`SIGKILL`), and using `trap` to intercept signals
- **Process control by name**: `pkill -f` for finding and signaling processes without knowing their PID in advance
- **Detaching processes from a session**: `nohup` and background execution (`&`) for processes that need to outlive their parent shell
- **Daemon conventions**: writing a PID file so external tooling can manage a long-running process
- **Low-level process lifecycle**: `fork()`/`exit()`/`wait()` at the C level, and what a zombie process actually is under the hood

## Why This Matters Beyond the Exercises

Every "restart the service," "why won't this process die," and "is this actually still running" question in real operations comes back to the concepts in this module. Knowing the difference between `SIGTERM` and `SIGKILL` alone has saved me from ever reaching for `kill -9` as a first resort — a graceful shutdown that gives a process a chance to close connections and flush data properly is almost always the right first move, with a hard kill as the deliberate fallback, not the default.

## Requirements

- Ubuntu 16.04/20.04 LTS
- Bash
- A C compiler (`gcc`) for `102-zombie.c`

## Author

**SwissKnifeTech** — ALX System Engineering & DevOps track
