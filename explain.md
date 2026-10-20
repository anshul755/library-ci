# Practical 09 – Explanation (for sir / viva)

## Aim
Whenever code changes, something that worked may break. Instead of testing by hand each time,
a pipeline **automatically runs the tests after every change** and reports pass or fail.
This is continuous testing.

## Why GitHub Actions instead of Jenkins?
Jenkins is an automation server that needs Java, installation, plugins and setup, and cannot receive
GitHub's push notifications from a laptop without extra network work. GitHub Actions is GitHub's built-in
CI service: nothing to install, and the pipeline starts on its own at every push (the "automatic trigger"
part of the manual). The concept is the same: Checkout -> Install -> Test -> Result.

## Project
A library lending system (not a calculator): members borrow books, each has a loan limit, and if no copy is
left they join a waiting list. A returned book goes to the first person waiting (FIFO).
8 PyTest cases: normal borrow, unknown book, waiting list, loan limit, duplicate borrow,
FIFO hand-over on return, restock on return, returning a book not borrowed.

## Flow
1. Wrote code and tests; the code is stored in a GitHub repo (`git push`).
2. The push triggers the workflow `ci.yml`. GitHub starts a fresh Ubuntu machine and runs the steps:
   Checkout (download the latest code), Setup Python, Install Dependencies (pytest from `requirements.txt`),
   Run Tests (`pytest`). Run #1: 8 passed -> green.
3. Failure demo: I introduced a bug (`queue.pop()` instead of `queue.pop(0)`, so the last waiting person
   is served first) and pushed. The pipeline ran by itself, `test_return_hands_book_to_first_in_queue` failed
   (`'meera' == 'ravi'`) -> red. The bug was found without anyone testing manually.
4. Fix: restored `queue.pop(0)`, pushed, pipeline reran -> green.

Cycle: code change -> automatic pipeline -> automated tests -> result -> fix -> repeat.

## How is pass/fail decided?
By the exit code of `pytest`: 0 = all passed, non-zero = some failed. Actions marks the step and run accordingly.
GitHub Actions does not test anything itself; PyTest tests, Actions only triggers and reports.

## Where do tests run?
On a GitHub-hosted virtual machine (`ubuntu-latest`), on a fresh copy of the committed code.

## Viva Q&A
- **CI / continuous testing?** Automatically building and testing code on every change to find defects early.
- **Roles?** Git tracks changes; GitHub stores the repo and (via Actions) runs the pipeline; PyTest runs tests.
- **Workflow / job / step / run?** Pipeline file; group of steps on one machine; a single command/action; one execution.
- **`on: push` meaning?** The workflow starts whenever code is pushed to the listed branch.
- **Why did the run fail in the demo?** Expected `ravi` but the buggy code returned `meera`.
- **Actions vs Jenkins?** Actions: hosted, no setup, YAML in the repo. Jenkins: self-hosted, more customisable, needs setup and maintenance.
- **Manual vs automatic trigger?** Manual: someone clicks Build Now. Automatic: a push/webhook starts it; Actions is automatic.
- **What is a webhook?** A message GitHub sends when an event (push) happens, to start a pipeline.
