# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`moodemoji` is a small, dependency-free Python library that maps mood strings to emoji. It exists mainly as a Python packaging exercise, so the packaging/release plumbing matters as much as the library code.

## Commands

```bash
pip install -e .          # editable install (required before running tests)
pytest                    # run all tests
pytest tests/test_core.py::test_mood_to_emoji   # run a single test
python -m build           # build sdist + wheel into dist/
```

There is no linter or formatter configured.

`happy.py` at the repo root is a scratch smoke-test script, not part of the package.

## Architecture

Data and logic are deliberately split across two modules:

- **`moodemoji/data.py`** — the vocabulary, and nothing else. `MOOD_CATEGORIES` is a dict of category → {mood: emoji} (370 canonical moods in 10 categories); `ALIASES` maps synonyms → canonical mood (934 of them), for 1,304 recognized terms in total.
- **`moodemoji/core.py`** — flattens `MOOD_CATEGORIES` into `MOOD_EMOJIS` at import time, then implements lookup on top of it.

Every lookup goes through the same path: `_normalize()` (lowercase, `_`/`-` → space, strip punctuation, collapse whitespace) → `ALIASES` resolution → `MOOD_EMOJIS` → `UNKNOWN_EMOJI` (🤔). Matching is deliberately **not** fuzzy — `"happpy"` returns 🤔 rather than guessing.

Two public APIs sit on that: functional (`mood_to_emoji`, `list_moods`, `list_all_terms`, `list_categories`) and class-based (`MoodInterpreter`). Anything public must be re-exported from `moodemoji/__init__.py`; tests and the README import from the package root, never from `moodemoji.core`.

### Editing the vocabulary

Add a mood as one entry in the appropriate `MOOD_CATEGORIES` category; add a synonym as one entry in `ALIASES`. The whole API picks up both automatically. Four invariants are enforced by tests in `tests/test_core.py` — breaking one fails the suite:

- No emoji is reused across canonical moods (if two moods want the same emoji, make one an alias of the other).
- Every `ALIASES` value is an existing canonical mood.
- No term is both canonical and an alias.
- Every term is already in normalized form (lowercase, no punctuation, single spaces).

`list_moods()` returns canonical moods only; synonyms are reachable via `mood_to_emoji()` and `list_all_terms()`.

## Backwards compatibility

`0.1.1` is published on PyPI, so a few things are contracts rather than implementation details:

- The seven original pairs — `happy 😊 · sad 😢 · angry 😠 · excited 🤩 · tired 😴 · love ❤️ · confused 😕` — must not change.
- The 🤔 fallback for unrecognized input.
- `mood_to_emoji`, `list_moods`, `MoodInterpreter` and their signatures. `list_moods()` gained an optional `category` argument; the no-argument call must keep working.
- `MOOD_EMOJIS` stays importable from `moodemoji.core` even though it's now derived.

The first three tests in `tests/test_core.py` are the original `0.1.x` tests, kept verbatim as a regression guard. Don't rewrite them.

## Releasing

Publishing is tag-driven via GitHub Actions; there is no manual `twine upload` step.

- `.github/workflows/publish.yml` — fires on `v*.*.*` tags, publishes to PyPI using the `PYPI_API_TOKEN` secret.
- `.github/workflows/testpypi.yml` — fires on `v*.*.*-beta*` / `-rc*` / `-alpha*` tags, publishes to TestPyPI using `TEST_PYPI_API_TOKEN`.

Bump `version` in `pyproject.toml` and tag to match before pushing a release. The version string is currently written with a leading `v` (`version = "v0.1.1"`); setuptools normalizes it, but prefer plain `0.1.1` for new bumps.
