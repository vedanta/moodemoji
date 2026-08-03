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

Everything lives in `moodemoji/core.py`, built around one module-level dict, `MOOD_EMOJIS`. Two APIs wrap it:

- Functional: `mood_to_emoji(mood)`, `list_moods()`
- Class-based: `MoodInterpreter`, which holds a `default_mood` and offers `get_emoji()` / `set_mood()` / `get_supported_moods()`

Both lowercase the input and fall back to 🤔 for unknown moods. Adding a mood means adding one entry to `MOOD_EMOJIS` — both APIs pick it up automatically. Anything meant to be public must be re-exported from `moodemoji/__init__.py`; tests and the README import from the package root, never from `moodemoji.core`.

Note: `core.py` currently defines `mood_to_emoji` and `list_moods` twice (identical bodies, the later pair wins). If you edit either function, edit both definitions or delete the duplicates.

## Releasing

Publishing is tag-driven via GitHub Actions; there is no manual `twine upload` step.

- `.github/workflows/publish.yml` — fires on `v*.*.*` tags, publishes to PyPI using the `PYPI_API_TOKEN` secret.
- `.github/workflows/testpypi.yml` — fires on `v*.*.*-beta*` / `-rc*` / `-alpha*` tags, publishes to TestPyPI using `TEST_PYPI_API_TOKEN`.

Bump `version` in `pyproject.toml` and tag to match before pushing a release. The version string is currently written with a leading `v` (`version = "v0.1.1"`); setuptools normalizes it, but prefer plain `0.1.1` for new bumps.
