# moodemoji/core.py

import re
from typing import List, Optional

from .data import ALIASES, MOOD_CATEGORIES

#: Flat mood -> emoji lookup, built from every category at import time.
MOOD_EMOJIS = {
    mood: emoji
    for moods in MOOD_CATEGORIES.values()
    for mood, emoji in moods.items()
}

#: Returned for anything we don't recognize.
UNKNOWN_EMOJI = "🤔"

_PUNCTUATION = re.compile(r"[^\w\s]", re.UNICODE)
_WHITESPACE = re.compile(r"\s+")


def _normalize(text: str) -> str:
    """Fold user input into a lookup key.

    Lowercases, treats ``_`` and ``-`` as spaces, drops punctuation and
    collapses runs of whitespace, so ``"  HAPPY! "`` and ``"very_happy"``
    both come out clean. Nothing fuzzy happens here -- a typo stays a typo
    and ends up on the UNKNOWN_EMOJI path.
    """
    text = text.lower().replace("_", " ").replace("-", " ")
    text = _PUNCTUATION.sub("", text)
    return _WHITESPACE.sub(" ", text).strip()


def _resolve(mood: str) -> str:
    """Normalize a term and follow it through ALIASES to a canonical mood."""
    key = _normalize(mood)
    return ALIASES.get(key, key)


def mood_to_emoji(mood: str) -> str:
    """Return the emoji for a mood, or 🤔 if we don't know it."""
    return MOOD_EMOJIS.get(_resolve(mood), UNKNOWN_EMOJI)


def list_moods(category: Optional[str] = None) -> List[str]:
    """Canonical mood names, sorted. Pass a category to narrow it down."""
    if category is None:
        return sorted(MOOD_EMOJIS)

    key = _normalize(category)
    if key not in MOOD_CATEGORIES:
        raise ValueError(
            "unknown category {!r}; expected one of: {}".format(
                category, ", ".join(sorted(MOOD_CATEGORIES))
            )
        )
    return sorted(MOOD_CATEGORIES[key])


def list_all_terms() -> List[str]:
    """Every term we recognize -- canonical moods plus all their synonyms."""
    return sorted(set(MOOD_EMOJIS) | set(ALIASES))


def list_categories() -> List[str]:
    """The mood families, sorted."""
    return sorted(MOOD_CATEGORIES)


class MoodInterpreter:
    """Holds a default mood so you don't have to pass one every time."""

    def __init__(self, default_mood: str = "happy"):
        self.default_mood = _normalize(default_mood)

    def get_emoji(self, mood: Optional[str] = None) -> str:
        """Emoji for ``mood``, falling back to the interpreter's default."""
        return mood_to_emoji(mood if mood is not None else self.default_mood)

    def set_mood(self, mood: str):
        self.default_mood = _normalize(mood)

    def get_supported_moods(self) -> List[str]:
        return list_moods()
