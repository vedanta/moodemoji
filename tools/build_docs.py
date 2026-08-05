#!/usr/bin/env python3
"""Regenerate the docs that are derived from ``moodemoji/data.py``.

Two things in this repo are generated rather than hand-written, and both go
stale the moment the vocabulary changes:

* ``docs/index.html`` -- the GitHub Pages emoji reference
* the mood tables in ``README.md``, between the ``BEGIN/END GENERATED`` markers

Run this after editing the vocabulary::

    python tools/build_docs.py            # rewrite both
    python tools/build_docs.py --check    # exit 1 if either is out of date

``--check`` writes nothing, so it is safe to wire into CI as a guard against
someone editing data.py and forgetting the docs.
"""

import argparse
import collections
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moodemoji.data import ALIASES, MOOD_CATEGORIES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
PAGE = os.path.join(ROOT, "docs", "index.html")

BEGIN = "<!-- BEGIN GENERATED: mood tables"
END = "<!-- END GENERATED: mood tables -->"

# Display order and one-line blurbs. Deliberately not alphabetical -- this is
# the order a reader should meet the categories in.
ORDER = [
    "positive",
    "negative",
    "energy",
    "social",
    "cognitive",
    "physical",
    "playful",
    "neutral",
    "slang",
    "existential",
]
DESC = {
    "positive": "feeling good",
    "negative": "feeling bad",
    "energy": "how much gas is in the tank",
    "social": "feelings about other people",
    "cognitive": "what your brain is doing",
    "physical": "what your body is doing",
    "playful": "being a menace",
    "neutral": "level, in-between states",
    "slang": "internet and modern shorthand",
    "existential": "the big questions",
}

MAX_SYNONYMS_SHOWN = 4


def vocabulary():
    """Flat mood->emoji map, synonyms grouped by the mood they point at."""
    missing = set(MOOD_CATEGORIES) ^ set(ORDER)
    if missing:
        raise SystemExit(
            "ORDER/DESC in this script are out of sync with data.py: {}".format(
                ", ".join(sorted(missing))
            )
        )
    flat = {m: e for moods in MOOD_CATEGORIES.values() for m, e in moods.items()}
    by_mood = collections.defaultdict(list)
    for alias, target in ALIASES.items():
        by_mood[target].append(alias)
    return flat, by_mood


def synonyms_cell(by_mood, mood):
    found = sorted(by_mood.get(mood, []))
    if not found:
        return "—"
    cell = ", ".join("`{}`".format(a) for a in found[:MAX_SYNONYMS_SHOWN])
    if len(found) > MAX_SYNONYMS_SHOWN:
        cell += ", …"
    return cell


def render_readme_tables(by_mood):
    out = []
    for cat in ORDER:
        moods = MOOD_CATEGORIES[cat]
        out.append("### `{}` — {} ({} moods)".format(cat, DESC[cat], len(moods)))
        out.append("")
        out.append("| Emoji | Mood | Also accepts |")
        out.append("|:---:|---|---|")
        for mood in sorted(moods):
            out.append(
                "| {} | `{}` | {} |".format(
                    moods[mood], mood, synonyms_cell(by_mood, mood)
                )
            )
        out.append("")
    return "\n".join(out).rstrip()


def build_readme(current, flat, by_mood):
    """Return README text with tables and inline counts refreshed."""
    start = current.index(BEGIN)
    start = current.index("\n", start) + 1
    end = current.index(END)
    updated = current[:start] + "\n" + render_readme_tables(by_mood) + "\n\n" + current[end:]

    n_moods, n_aliases = len(flat), len(ALIASES)
    n_terms = n_moods + n_aliases
    n_cats = len(MOOD_CATEGORIES)
    words = {8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}

    # Counts quoted in the prose. Patterns are digit-agnostic so this keeps
    # working as the vocabulary grows.
    substitutions = [
        (r"\*\*[\d,]+ mood words\*\* — \d+ core moods plus \d+ synonyms",
         "**{:,} mood words** — {} core moods plus {} synonyms".format(
             n_terms, n_moods, n_aliases)),
        (r"returns all \d+ core mood names",
         "returns all {} core mood names".format(n_moods)),
        (r"len\(list_moods\(\)\)      # \d+",
         "len(list_moods())      # {}".format(n_moods)),
        (r"len\(list_moods\(\)\)       # \d+  core moods",
         "len(list_moods())       # {}  core moods".format(n_moods)),
        (r"len\(list_all_terms\(\)\)   # \d+  core moods \+ synonyms",
         "len(list_all_terms())   # {}  core moods + synonyms".format(n_terms)),
        (r"len\(list_moods\(\"positive\"\)\)  # \d+",
         'len(list_moods("positive"))  # {}'.format(len(MOOD_CATEGORIES["positive"]))),
        (r"`list_categories\(\)` — the \w+ mood families",
         "`list_categories()` — the {} mood families".format(
             words.get(n_cats, str(n_cats)))),
    ]
    for pattern, replacement in substitutions:
        updated, n = re.subn(pattern, replacement, updated)
        if n != 1:
            raise SystemExit(
                "README pattern matched {} times (expected 1): {}".format(n, pattern)
            )
    return updated


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>moodemoji &mdash; every mood, every emoji</title>
<meta name="description" content="All {n_moods} moods in the moodemoji Python \
library. Hover any emoji to see its mood.">
<style>
  :root {{
    --bg: #0d1117;
    --surface: #161b22;
    --border: #30363d;
    --text: #e6edf3;
    --muted: #8b949e;
    --accent: #58a6ff;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 48px 24px 72px;
    background: var(--bg);
    color: var(--text);
    font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica,
          Arial, sans-serif;
  }}
  .wrap {{ max-width: 900px; margin: 0 auto; }}
  header {{ margin-bottom: 48px; }}
  h1 {{ margin: 0 0 8px; font-size: 32px; letter-spacing: -0.02em; }}
  .tagline {{ margin: 0 0 20px; color: var(--muted); font-size: 18px; }}
  .stats {{ color: var(--muted); font-size: 14px; margin: 0 0 20px; }}
  .stats b {{ color: var(--text); }}
  code {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 6px; padding: 2px 6px; font-size: 14px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  }}
  a {{ color: var(--accent); }}
  h2 {{
    font-size: 15px; text-transform: uppercase; letter-spacing: 0.08em;
    margin: 40px 0 14px; padding-bottom: 8px;
    border-bottom: 1px solid var(--border); font-weight: 600;
  }}
  h2 .count {{
    text-transform: none; letter-spacing: 0; color: var(--muted);
    font-weight: 400; font-size: 13px; float: right; padding-top: 2px;
  }}
  .grid {{
    display: grid; gap: 8px;
    grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
  }}
  .tile {{
    position: relative; aspect-ratio: 1; display: flex;
    align-items: center; justify-content: center;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; cursor: default; outline: none;
    transition: border-color .12s ease, transform .12s ease;
  }}
  .emoji {{ font-size: 26px; line-height: 1; }}
  .tile:hover, .tile:focus {{
    border-color: var(--accent); transform: translateY(-2px); z-index: 3;
  }}
  /* the mood name, revealed on hover or keyboard focus */
  .tile::after {{
    content: attr(data-mood);
    position: absolute; bottom: calc(100% + 8px); left: 50%;
    transform: translateX(-50%);
    background: #1f6feb; color: #fff;
    padding: 5px 9px; border-radius: 6px;
    font-size: 12px; line-height: 1.2; white-space: nowrap;
    opacity: 0; pointer-events: none;
    transition: opacity .12s ease;
  }}
  .tile:hover::after, .tile:focus::after {{ opacity: 1; }}
  footer {{
    margin-top: 56px; padding-top: 20px; border-top: 1px solid var(--border);
    color: var(--muted); font-size: 14px;
  }}
  @media (max-width: 480px) {{
    body {{ padding: 32px 16px 56px; }}
    h2 .count {{ float: none; display: block; padding-top: 4px; }}
  }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>🎭 moodemoji</h1>
    <p class="tagline">Give it a mood, get an emoji back.</p>
    <p class="stats">
      <b>{n_moods}</b> moods in <b>{n_cats}</b> categories &middot;
      <b>{n_terms}</b> recognized terms once synonyms are counted &middot;
      hover any tile to see its mood
    </p>
    <p><code>pip install moodemoji</code></p>
  </header>

{sections}

  <footer>
    Generated from the library's own vocabulary &middot;
    <a href="https://github.com/vedanta/moodemoji">GitHub</a> &middot;
    <a href="https://pypi.org/project/moodemoji/">PyPI</a>
  </footer>
</div>
</body>
</html>
"""


def build_page(flat):
    sections = []
    for cat in ORDER:
        moods = MOOD_CATEGORIES[cat]
        tiles = []
        for mood in sorted(moods):
            label = html.escape(mood)
            tiles.append(
                '        <div class="tile" tabindex="0" data-mood="{label}" '
                'title="{label}"><span class="emoji">{emoji}</span></div>'.format(
                    label=label, emoji=moods[mood]
                )
            )
        sections.append(
            """    <section>
      <h2>{cat} <span class="count">{n} moods &middot; {desc}</span></h2>
      <div class="grid">
{tiles}
      </div>
    </section>""".format(
                cat=cat,
                n=len(moods),
                desc=html.escape(DESC[cat]),
                tiles="\n".join(tiles),
            )
        )
    return PAGE_TEMPLATE.format(
        n_moods=len(flat),
        n_terms=len(flat) + len(ALIASES),
        n_cats=len(MOOD_CATEGORIES),
        sections="\n\n".join(sections),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the docs are up to date without writing; exit 1 if not",
    )
    args = parser.parse_args()

    flat, by_mood = vocabulary()
    targets = [
        (README, build_readme(open(README).read(), flat, by_mood)),
        (PAGE, build_page(flat)),
    ]

    stale = [path for path, new in targets if open(path).read() != new]

    if args.check:
        if stale:
            print("out of date: {}".format(", ".join(os.path.basename(p) for p in stale)))
            print("run: python tools/build_docs.py")
            return 1
        print("docs are up to date ({} moods, {} terms)".format(
            len(flat), len(flat) + len(ALIASES)))
        return 0

    for path, new in targets:
        with open(path, "w") as fh:
            fh.write(new)
    print("wrote README.md and docs/index.html: {} moods in {} categories, "
          "{} terms".format(len(flat), len(MOOD_CATEGORIES), len(flat) + len(ALIASES)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
