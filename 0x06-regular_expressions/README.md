# 0x06. Regular Expressions

This module is a deliberate change of tools: instead of Bash, every script here is written in **Ruby**, specifically to practice regular expressions using a language with clean, readable regex syntax (`/pattern/`) built directly into the language, rather than shelling out to `grep`/`sed` with their more cryptic POSIX regex dialects. The underlying skill — describing a *pattern* of text rather than a literal string — is completely transferable back to `grep -E`, `sed`, log-parsing tools, and just about every language you'll use professionally.

Regex is one of those skills that looks intimidating from a distance and becomes genuinely fast once it clicks. This module is where it clicked for me — one small building block (a literal match, then a repetition token, then an anchor, then a capture group) at a time, rather than trying to write a complex pattern from scratch on day one.

## The Core Concepts

**A pattern, not a string** — `/hello/` doesn't mean "the text hello," it means "match this sequence of characters wherever it appears." Regex lets you describe *shapes* of text ("three digits, a dash, three more digits") instead of only exact strings.

**Repetition tokens** — the real power of regex over plain string matching:
| Token | Meaning |
|---|---|
| `?` | zero or one of the preceding element |
| `*` | zero or more |
| `+` | one or more |
| `{n,m}` | between `n` and `m` repetitions |

**Anchors** — `^` and `$` pin a match to the **start** and **end** of a string/line, respectively, turning "contains this pattern" into "consists entirely of this pattern" when combined.

**Capture groups** — `(...)` (or `(?<name>...)` for a *named* group) don't just match a portion of text, they let you **extract** it afterward — turning regex from a yes/no matcher into a real parsing tool.

**Ruby regex mechanics used throughout this module:**
- `/pattern/` — a regex literal
- `str =~ /pattern/` — returns the index of the first match, or `nil` if there isn't one (frequently used just as a truthy/falsy check)
- `str.match(/pattern/)` — returns a `MatchData` object with full details about the match, including captured groups
- `str.gsub(/pattern/) { |match| ... }` — global substitution, replacing every match, optionally computed by a block instead of a fixed string

---

## Task-by-Task Breakdown

### 0. `0-simply_match_school.rb` — done
**Concept:** a basic literal match

```ruby
if STDIN.gets.chomp =~ /School/
  puts "Yes"
else
  puts "No"
end
```
The simplest possible regex: check whether the literal word "School" appears anywhere in the input line. `=~` returns the match position (truthy) or `nil` (falsy), which is exactly what an `if` check needs. This is the "hello world" of regex — proving the matching mechanism works before adding any complexity.

### 1. `1-repetition_token_0.rb` — done
**Concept:** the `?` token (zero or one)

```ruby
/hbtn?/
```
Matches "hbt" **or** "hbtn" — the `?` makes the preceding character (`n`) optional. This is the first real regex "aha" moment: one pattern matching two different literal strings, because you've described a *shape* instead of writing both strings out and checking each separately.

### 2. `2-repetition_token_1.rb` — done
**Concept:** the `+` token (one or more)

```ruby
/hbt+n/
```
Matches "hbtn," "hbttn," "hbtttn," and so on — one or more `t` characters between `hb` and `n`. `+` is what you reach for when something is *required* but can repeat — a very common real pattern for things like matching one-or-more whitespace characters or digits.

### 3. `3-repetition_token_2.rb` — done
**Concept:** the `*` token (zero or more)

```ruby
/hbt*n/
```
Similar to task 2, but now `t` is entirely optional — "hbn" also matches, alongside "hbtn," "hbttn," etc. The distinction between `+` (at least one) and `*` (zero is fine) is small syntactically but significant semantically — mixing them up is a common regex bug.

### 4. `4-repetition_token_3.rb` — done
**Concept:** the `{n,m}` bounded quantifier

```ruby
/hbt{2,3}n/
```
Matches only when `t` repeats **between 2 and 3 times** — no more, no fewer. This is the precise version of `*`/`+`, useful whenever a format has a known, fixed range — e.g. validating that a ZIP code has exactly 5 digits, or a product code has 3 to 5 characters.

### 5. `5-beginning_and_end.rb` — done
**Concept:** anchors `^` and `$`

```ruby
/^hbtn$/
```
Without anchors, a pattern matches if it appears *anywhere* in the string — including as part of a longer word. Wrapping it in `^...$` forces the **entire** string to consist of exactly that pattern, nothing before or after. This distinction matters constantly in validation: "contains a number" and "is entirely a number" are very different checks, and anchors are what separate them.

### 6. `6-phone_number.rb` — done
**Concept:** a realistic validation pattern

```ruby
/^\d{3}-\d{3}-\d{4}$/
```
Combines everything above into something genuinely useful: validating that a string is a US-style phone number, exactly — three digits, a dash, three digits, a dash, four digits, with anchors ensuring there's nothing extra before or after. `\d` is shorthand for `[0-9]`. This is the module's first task that looks like something you'd actually ship in a real form-validation or data-cleaning script.

### 7. `7-OMG_WHY_ARE_YOU_SHOUTING.rb` — done
**Concept:** `gsub` with a block, character classes

```ruby
str.gsub(/[A-Z]/) { |letter| letter.downcase }
```
`[A-Z]` is a **character class** — matches any single uppercase letter (as an alternative to writing `A|B|C|...`). `gsub` with a block calls that block for **every match**, letting you compute the replacement dynamically (here, lowercasing each matched letter) instead of substituting a fixed string. This is the pattern behind a huge range of real text-cleaning tasks: normalizing case, redacting sensitive substrings, or reformatting matched data on the fly.

### 100. `100-textme.rb` — done (bonus)
**Concept:** named capture groups, extracting structured data

```ruby
line = "[2016-03-08 20:54:15] 042526082 :: 033336789 :: Hello"
if line =~ /^\[(?<date>.*)\] (?<from>\d+) :: (?<to>\d+) :: (?<message>.*)$/
  puts "#{$~[:from]} sent #{$~[:to]} \"#{$~[:message]}\""
end
```
The capstone task: parsing a structured log line into its individual components using **named capture groups** (`(?<name>...)`), then referencing each captured piece by name (`$~[:from]`) instead of a positional index. This is real-world log parsing — the exact technique used to pull structured fields (timestamps, IPs, usernames, messages) out of raw text logs, which is a genuinely everyday task in monitoring, debugging, and building alerting rules.

---

## Skills Demonstrated in This Module

- **Pattern thinking**: describing the *shape* of valid text instead of enumerating every literal possibility
- **Quantifiers**: `?`, `+`, `*`, `{n,m}` and knowing precisely which one expresses a given requirement
- **Anchoring**: `^`/`$` to control whether a pattern matches a substring or the whole string
- **Character classes**: `[A-Z]`, `\d` and similar shorthand for "any character from this set"
- **Capture groups**: both positional and **named** (`(?<name>...)`), for extracting structured data out of unstructured text
- **Practical Ruby regex methods**: `=~` for boolean checks, `.match` for detail, `.gsub` (with a block) for dynamic substitution

## Why This Matters Beyond the Exercises

Regex shows up everywhere in real infrastructure work: `grep -E` for filtering logs during an incident, validation rules in application code, `nginx`/Apache rewrite rules, CI pipeline log parsing, and monitoring alert rules that match on error patterns. Learning it properly here — building complexity one token at a time in a language with clean regex syntax — made it something I actually reach for confidently, instead of copy-pasting a pattern from Stack Overflow and hoping it works.

## Requirements

- Ruby (any recent 2.x/3.x interpreter)
- Ubuntu 16.04/20.04 LTS

## Author

**SwissKnifeTech** — ALX System Engineering & DevOps track
