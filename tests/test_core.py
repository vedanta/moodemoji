# tests/test_core.py

import pytest

from moodemoji import (
    MoodInterpreter,
    list_all_terms,
    list_categories,
    list_moods,
    mood_to_emoji,
)
from moodemoji.core import MOOD_EMOJIS, UNKNOWN_EMOJI
from moodemoji.data import ALIASES, MOOD_CATEGORIES

# --- original 0.1.x tests, unchanged: these are the compatibility contract ---


def test_mood_to_emoji():
    assert mood_to_emoji("happy") == "😊"
    assert mood_to_emoji("unknown") == "🤔"


def test_list_moods():
    assert "happy" in list_moods()


def test_mood_interpreter_class():
    mi = MoodInterpreter("sad")
    assert mi.get_emoji() == "😢"
    assert mi.get_emoji("excited") == "🤩"
    mi.set_mood("tired")
    assert mi.get_emoji() == "😴"
    assert "love" in mi.get_supported_moods()


# --- backwards compatibility ------------------------------------------------

ORIGINAL_MOODS = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "excited": "🤩",
    "tired": "😴",
    "love": "❤️",
    "confused": "😕",
}


@pytest.mark.parametrize("mood,emoji", sorted(ORIGINAL_MOODS.items()))
def test_original_moods_keep_their_emoji(mood, emoji):
    assert mood_to_emoji(mood) == emoji


def test_readme_examples_still_hold():
    assert mood_to_emoji("tired") == "😴"
    assert mood_to_emoji("curious") == "🤔"


# --- aliases ----------------------------------------------------------------


def test_aliases_resolve_to_their_canonical_emoji():
    assert mood_to_emoji("elated") == mood_to_emoji("joyful")
    assert mood_to_emoji("glad") == "😊"
    assert mood_to_emoji("furious") == mood_to_emoji("livid")


def test_every_alias_points_at_a_canonical_mood():
    unknown = {a: t for a, t in ALIASES.items() if t not in MOOD_EMOJIS}
    assert unknown == {}


def test_no_term_is_both_canonical_and_alias():
    assert set(ALIASES) & set(MOOD_EMOJIS) == set()


def test_list_all_terms_covers_moods_and_aliases():
    terms = set(list_all_terms())
    assert terms == set(MOOD_EMOJIS) | set(ALIASES)
    assert terms > set(list_moods())


# --- normalization ----------------------------------------------------------


@pytest.mark.parametrize(
    "text", ["happy", "HAPPY", "  happy  ", "Happy!", "  HAPPY! ", "happy."]
)
def test_normalization_variants(text):
    assert mood_to_emoji(text) == "😊"


def test_normalization_handles_separators():
    assert mood_to_emoji("burnt_out") == mood_to_emoji("burnt out")
    assert mood_to_emoji("burnt-out") == mood_to_emoji("burnt out")


def test_typos_are_not_guessed():
    for text in ["happpy", "banana", "", "asdfgh"]:
        assert mood_to_emoji(text) == UNKNOWN_EMOJI


# --- categories -------------------------------------------------------------


def test_list_categories():
    assert list_categories() == sorted(MOOD_CATEGORIES)
    assert "positive" in list_categories()


def test_category_moods_are_a_subset_of_all_moods():
    every = set(list_moods())
    for category in list_categories():
        subset = set(list_moods(category))
        assert subset
        assert subset <= every


def test_categories_partition_the_moods():
    combined = [m for c in list_categories() for m in list_moods(c)]
    assert sorted(combined) == list_moods()  # no overlap, nothing missing


def test_unknown_category_raises():
    with pytest.raises(ValueError) as excinfo:
        list_moods("nonsense")
    assert "positive" in str(excinfo.value)


def test_category_argument_is_normalized():
    assert list_moods("  POSITIVE ") == list_moods("positive")


# --- data invariants --------------------------------------------------------


def test_every_canonical_mood_has_a_unique_emoji():
    seen = {}
    for mood, emoji in MOOD_EMOJIS.items():
        assert emoji not in seen, "{} and {} share {}".format(
            seen.get(emoji), mood, emoji
        )
        seen[emoji] = mood


def test_terms_are_already_normalized():
    from moodemoji.core import _normalize

    for term in list_all_terms():
        assert term == _normalize(term)


def test_vocabulary_is_exhaustive():
    assert len(list_moods()) >= 350
    assert len(list_all_terms()) >= 1250
    assert len(list_categories()) >= 10


# --- MoodInterpreter --------------------------------------------------------


def test_interpreter_understands_aliases_and_normalization():
    mi = MoodInterpreter("  ELATED! ")
    assert mi.get_emoji() == mood_to_emoji("joyful")
    mi.set_mood("livid")
    assert mi.get_emoji() == mood_to_emoji("furious")
    assert mi.get_emoji("Sad!") == "😢"


def test_interpreter_defaults_to_happy():
    assert MoodInterpreter().get_emoji() == "😊"


def test_interpreter_unknown_mood_falls_back():
    assert MoodInterpreter("banana").get_emoji() == UNKNOWN_EMOJI
