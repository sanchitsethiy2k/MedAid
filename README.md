# MedAid

A command-line medication adherence tracker built in Python, originally started as a course final project and extended well past that scope based on where I wanted to take it.

## Why I built this

I live with an illness that requires strict daily medication adherence, and I know firsthand how easy it is to lose track of doses even when you're actively trying not to. That personal experience shaped this project from the start.

Before writing any code, I asked why people actually miss doses. Three reasons kept coming up: they don't realize a medication is about to run out until it's too late; they lose track of whether they took a dose on a given day, especially across multiple meds and multiple daily doses; and cost — medications sometimes get skipped or stretched out because they're expensive. MedAid is built to directly address each of these.

## Features

Refill tracking. Every medication has a running dose count that decrements automatically on each logged intake. A stock alert prints once doses drop to 5 or below, and once a medication hits zero, logging is blocked for it until it's refilled — surfacing the problem before it becomes a missed dose, instead of relying on memory.

Dose logging & adherence history. Logging prompts dose-by-dose based on each medication's daily frequency, recording a timestamped Y/N entry to a persistent log file. A history view prints the full log alongside a calculated adherence percentage per medication, so the pattern is visible at a glance rather than buried in raw entries.

Generic drug cost comparison. Enter an active ingredient, strength, and price paid, and MedAid checks it against a reference CSV to flag cheaper generic equivalents and by how much — aimed at removing cost as a silent reason people ration medication.

Add / refill / remove management. Medications can be added one at a time, refilled by selecting from a numbered list, or removed the same way, with the underlying CSV rewritten after each change so the file on disk always reflects current state.

## Design choices

Built around two classes, Patient and Med, which mapped naturally onto the data — patient identity and medication data are genuinely distinct things — and gave me a real reason to get comfortable with OOP rather than knowing it only on paper.

Input validation uses raise rather than having each validator print an error and return None. Each validator's only job is deciding valid or not — if the input fails, it raises a ValueError. The calling code wraps the validator in a while True loop with try/except: the try block calls the validator and breaks out of the loop on success, while the except block prints a message describing exactly what was wrong and continues to re-prompt. This keeps the validators themselves simple, with all the re-prompting and user-facing messaging living in one consistent place in the loop.

Med construction is split into two paths rather than one. Early on, a single method tried to handle both building a fresh medication list from user input and reconstructing one from a saved CSV, which tangled interactive prompting into a path that didn't need it. I split this into get_meds, which only handles the new-entry flow, and a separate load classmethod that rebuilds a Med purely from stored data with no prompting involved — main() decides which path to call based on whether a medication file already exists for the patient. Refill and remove are handled as their own methods on Med as well, so the logic for what counts as a valid refill amount or how a medication gets dropped from the list lives in exactly one place rather than being duplicated across call sites.

Adherence percentage is derived from the log file itself rather than tracked as a running counter — history() reads every logged row for a given medication, counts how many were taken versus total logged, and computes the percentage from that. This means the log is the single source of truth for adherence, instead of adherence being a second value that could drift out of sync with what was actually logged.

## Files

medaid.py — Patient and Med classes, main() menu loop, the add/refill/remove submenu, the generic-cost lookup, and the input validators

test_medaid.py — tests for the validation functions

generic_med.csv — reference database of active ingredients, strengths, and costs used by the generic-alternative feature
