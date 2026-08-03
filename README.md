# 🎭 moodemoji

**Give it a mood, get an emoji back.**

```python
>>> from moodemoji import mood_to_emoji
>>> mood_to_emoji("happy")
'😊'
```

That's the whole idea. `moodemoji` knows **553 mood words** — 147 core moods plus 406 synonyms — and maps each one to a fitting emoji. It has no dependencies, needs no setup, and never raises on unknown input.

---

## 📋 Requirements

- Python 3.7 or newer
- Nothing else — `moodemoji` has zero dependencies

---

## 📦 Installation

```bash
pip install moodemoji
```

To work on the library itself, clone the repo and install it in *editable* mode, which means your changes take effect immediately without reinstalling:

```bash
git clone https://github.com/vedanta/moodemoji.git
cd moodemoji
pip install -e .
```

---

## ⚡ Quick start

Open a Python prompt and try this:

```python
from moodemoji import mood_to_emoji

print(mood_to_emoji("happy"))    # 😊
print(mood_to_emoji("tired"))    # 😴
print(mood_to_emoji("elated"))   # 😄  a synonym for "joyful"
print(mood_to_emoji("banana"))   # 🤔  not a mood, so you get the shrug
```

Three things to notice:

1. **It never crashes.** Anything unrecognized returns 🤔 instead of raising an error, so you can pass user input straight in.
2. **Synonyms work.** You don't have to know the exact word — `"elated"`, `"overjoyed"` and `"jubilant"` all resolve to the same emoji.
3. **Messy input is fine.** `"  HAPPY!  "` works just as well as `"happy"`.

---

## 🧑‍💻 Detailed usage

There are two ways to use the library. Start with the functions — the class is only worth it if you're looking up the same mood repeatedly.

### The functional API

#### `mood_to_emoji(mood)` — the one you'll actually use

Takes a mood word, returns an emoji as a string.

```python
from moodemoji import mood_to_emoji

mood_to_emoji("grateful")   # '🙏'
mood_to_emoji("burnt out")  # '🕯️'
mood_to_emoji("qwerty")     # '🤔'  unknown -> fallback
```

Because it always returns a string, it drops straight into f-strings:

```python
mood = input("How are you feeling? ")
print(f"You seem {mood} {mood_to_emoji(mood)}")
```

#### `list_moods(category=None)` — see what's available

With no arguments, returns all 147 core mood names, alphabetically sorted:

```python
from moodemoji import list_moods

list_moods()           # ['achy', 'adventurous', 'affectionate', ...]
len(list_moods())      # 147
```

Pass a category name to narrow it down:

```python
list_moods("positive")   # ['amused', 'awestruck', 'blissful', ...]
len(list_moods("positive"))  # 25
```

If you pass a category that doesn't exist, you get a helpful `ValueError` rather than a silent empty list:

```python
list_moods("vibes")
# ValueError: unknown category 'vibes'; expected one of: cognitive,
# energy, negative, neutral, physical, playful, positive, social
```

#### `list_categories()` — the eight mood families

```python
from moodemoji import list_categories

list_categories()
# ['cognitive', 'energy', 'negative', 'neutral',
#  'physical', 'playful', 'positive', 'social']
```

Handy for looping over everything:

```python
from moodemoji import list_categories, list_moods, mood_to_emoji

for category in list_categories():
    print(f"\n{category.upper()}")
    for mood in list_moods(category):
        print(f"  {mood_to_emoji(mood)}  {mood}")
```

#### `list_all_terms()` — including every synonym

`list_moods()` gives you core moods only, so the list stays readable. When you want *everything* the library recognizes — synonyms included — use `list_all_terms()`:

```python
from moodemoji import list_all_terms, list_moods

len(list_moods())       # 147  core moods
len(list_all_terms())   # 553  core moods + synonyms
```

This is the list to check against if you want to know whether a word is recognized:

```python
if "stoked" in list_all_terms():
    print("recognized!")   # it is — a synonym for "excited"
```

### The class-based API

`MoodInterpreter` remembers a mood for you, so you don't have to pass one on every call. Reach for it when you're tracking someone's current mood over time.

```python
from moodemoji import MoodInterpreter

mi = MoodInterpreter("excited")   # set a starting mood
mi.get_emoji()                    # '🤩'  uses the remembered mood

mi.set_mood("sad")                # change it
mi.get_emoji()                    # '😢'

mi.get_emoji("tired")             # '😴'  one-off, doesn't change the default
mi.get_emoji()                    # '😢'  still sad
```

| Method | What it does |
|---|---|
| `MoodInterpreter(default_mood="happy")` | Create one, optionally with a starting mood |
| `.get_emoji()` | Emoji for the remembered mood |
| `.get_emoji("angry")` | Emoji for a one-off mood, leaving the default alone |
| `.set_mood("calm")` | Change the remembered mood |
| `.get_supported_moods()` | Same list as `list_moods()` |

Synonyms and messy input work here too — `MoodInterpreter("  ELATED! ")` is understood.

---

## 🔍 How mood matching works

Every lookup goes through the same three steps.

**1. Your input is tidied up.** Uppercase becomes lowercase, punctuation is dropped, extra spaces collapse, and `_` and `-` count as spaces:

| You pass | Treated as |
|---|---|
| `"HAPPY"` | `happy` |
| `"  happy  "` | `happy` |
| `"Happy!"` | `happy` |
| `"burnt_out"` | `burnt out` |
| `"burnt-out"` | `burnt out` |

**2. Synonyms are resolved.** If the word is a synonym, it's swapped for its core mood — `"livid"` becomes `"furious"`, then looks up 🤬.

**3. Anything unrecognized returns 🤔.** Matching is exact, not fuzzy — this is deliberate. A typo like `"happpy"` gives you 🤔 rather than a confident guess, so the library never silently hands you the wrong emoji.

```python
mood_to_emoji("happpy")   # '🤔'  not '😊'
```

---

## 📖 All available moods and emojis

Every core mood, its emoji, and a few of the synonyms that map to it. Synonyms are shown in `code style`; where a mood has more than four, the rest are trimmed with `…`.

### `positive` — feeling good (25 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 😆 | `amused` | `entertained`, `tickled` |
| 🌟 | `awestruck` | `in awe`, `wonderstruck` |
| 😇 | `blissful` | `heavenly`, `serene bliss` |
| 😃 | `cheerful` | `bright`, `chipper`, `upbeat` |
| 💯 | `confident` | `assured`, `bold`, `self assured` |
| 🙂 | `content` | `at peace`, `comfortable`, `cosy`, `cozy`, … |
| 😁 | `delighted` | `chuffed` |
| 🎆 | `euphoric` | `elevated`, `smitten with life` |
| 🤩 | `excited` | `eager`, `enthusiastic`, `hyped`, `psyched`, … |
| 🎉 | `festive` | `celebratory`, `party` |
| 🤭 | `giddy` | `giggly` |
| 🙏 | `grateful` | `appreciative`, `blessed`, `thankful` |
| 😊 | `happy` | `glad`, `good`, `great`, `pleased`, … |
| 🌱 | `hopeful` | `encouraged`, `expectant` |
| 💡 | `inspired` | `creative spark` |
| 😄 | `joyful` | `elated`, `gleeful`, `jubilant`, `merry`, … |
| 🍀 | `lucky` | `fortunate` |
| 🔥 | `motivated` | `ambitious`, `driven`, `focused fire` |
| 🌈 | `optimistic` | `positive` |
| 🦚 | `proud` | `accomplished`, `dignified` |
| ✨ | `radiant` | `beaming`, `glowing` |
| 😮‍💨 | `relieved` | `reassured`, `unburdened` |
| 👌 | `satisfied` | `gratified` |
| 🎢 | `thrilled` | `exhilarated` |
| 🏆 | `triumphant` | `victorious`, `winning` |

### `negative` — feeling bad (32 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 😠 | `angry` | `cross`, `heated`, `mad` |
| 😤 | `annoyed` | `bothered`, `miffed`, `peeved` |
| 😰 | `anxious` | `apprehensive`, `jittery`, `nervous`, `on edge`, … |
| 🙈 | `ashamed` | `humiliated`, `mortified`, `sheepish` |
| 🗡️ | `betrayed` | `double crossed`, `stabbed in the back` |
| 🍋 | `bitter` | `cynical`, `jaded`, `sour` |
| 🏳️ | `defeated` | `beaten`, `demoralized`, `resigned` |
| 😔 | `depressed` | `despondent`, `low` |
| 😞 | `disappointed` | `disheartened`, `let down` |
| 🤢 | `disgusted` | `grossed out`, `repulsed`, `revolted` |
| 🫤 | `envious` | `covetous` |
| 😣 | `frustrated` | `annoyed at everything`, `exasperated`, `fed up` |
| 🤬 | `furious` | `enraged`, `irate`, `livid`, `seething` |
| 🥀 | `grieving` | `bereaved`, `mourning` |
| 😓 | `guilty` | `remorseful`, `sorry` |
| 💔 | `heartbroken` | `broken hearted`, `crushed`, `hurt`, `lovesick` |
| 🕳️ | `hopeless` | `despairing`, `helpless`, `lost` |
| 😧 | `horrified` | `aghast`, `appalled` |
| 🫥 | `insecure` | `inadequate`, `self conscious`, `unsure of myself` |
| 😖 | `irritated` | `agitated`, `cranky`, `grumpy`, `irked` |
| 🐍 | `jealous` | — |
| 😩 | `miserable` | `awful`, `terrible`, `wretched` |
| 🫠 | `numb` | `detached`, `dissociated`, `empty`, `hollow` |
| 😵 | `overwhelmed` | `buried`, `flooded`, `swamped` |
| 😳 | `panicked` | `alarmed`, `frantic`, `freaking out` |
| 😥 | `regretful` | `rueful`, `wistful` |
| 😾 | `resentful` | `begrudging`, `spiteful` |
| 😢 | `sad` | `blue`, `down`, `glum`, `melancholy`, … |
| 😨 | `scared` | `afraid`, `fearful`, `frightened`, `spooked` |
| 😫 | `stressed` | `strained`, `tense`, `under pressure` |
| 😱 | `terrified` | `horror struck`, `petrified` |
| 😟 | `worried` | `concerned`, `troubled` |

### `energy` — how much gas is in the tank (14 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 👀 | `alert` | `attentive`, `awake`, `sharp` |
| 🕯️ | `burnt out` | `burned out`, `burnout`, `crispy`, `fried` |
| 🪫 | `drained` | `depleted`, `running on empty` |
| ⚡ | `energized` | `charged`, `lively`, `peppy`, `vigorous` |
| 😪 | `exhausted` | `knackered`, `shattered`, `spent`, `wiped` |
| 🚀 | `hyper` | `bouncing`, `manic` |
| 🦥 | `lazy` | `idle`, `listless`, `unmotivated` |
| 🚿 | `refreshed` | `rejuvenated`, `renewed`, `revitalized` |
| 🛌 | `rested` | `fresh`, `restored` |
| 🌀 | `restless` | `antsy`, `fidgety`, `unsettled` |
| 💤 | `sleepy` | `dozy`, `drowsy` |
| 🐌 | `sluggish` | `heavy`, `slow` |
| 😴 | `tired` | `beat`, `fatigued`, `sleepy head`, `weary`, … |
| ☕ | `wired` | `buzzing`, `caffeinated` |

### `social` — feelings about other people (16 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 😘 | `affectionate` | `cuddly`, `tender`, `warm` |
| 💐 | `appreciated` | `seen`, `valued` |
| 😬 | `awkward` | `cringey`, `out of place`, `uncomfortable` |
| 😅 | `embarrassed` | `flustered`, `red faced` |
| 😉 | `flirty` | `coy`, `playful wink` |
| 🤝 | `friendly` | `amiable`, `kind`, `sociable` |
| 🐚 | `introverted` | `inward`, `withdrawn` |
| 🥺 | `lonely` | `abandoned`, `alone`, `homesick`, `isolated`, … |
| ❤️ | `love` | `adoring`, `in love`, `romantic`, `smitten` |
| 🥰 | `loved` | `adored`, `cherished`, `wanted` |
| 🗣️ | `outgoing` | `chatty`, `extroverted`, `gregarious` |
| 🛡️ | `protective` | `defensive`, `guarded` |
| 🫣 | `shy` | `bashful`, `reserved`, `timid` |
| 🫂 | `supported` | `backed up`, `cared for`, `held` |
| 🤞 | `trusting` | `hopeful in others`, `trustful` |
| 👋 | `welcoming` | `hospitable` |

### `cognitive` — what your brain is doing (17 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 🤯 | `amazed` | `astonished`, `dumbfounded`, `mind blown` |
| 🥱 | `bored` | `restive`, `tedious`, `understimulated` |
| 🤷 | `clueless` | `bewildered`, `lost the plot`, `no idea` |
| 😕 | `confused` | `baffled`, `disoriented`, `muddled`, `perplexed`, … |
| 🎨 | `creative` | `artistic`, `imaginative`, `inventive` |
| 🤔 | `curious` | `inquisitive`, `intrigued`, `nosy`, `wondering` |
| 💪 | `determined` | `persistent`, `resolute`, `stubborn`, `tenacious` |
| 🦋 | `distracted` | `scattered`, `spacey`, `unfocused` |
| 🧘 | `enlightened` | `awakened`, `centered`, `mindful` |
| 🎯 | `focused` | `absorbed`, `concentrated`, `dialed in`, `locked in` |
| 🌫️ | `forgetful` | `absent minded`, `foggy` |
| 🤨 | `indecisive` | `conflicted`, `on the fence`, `torn` |
| 🌪️ | `overthinking` | `in my head`, `ruminating`, `spiraling` |
| 😮 | `shocked` | `floored`, `speechless`, `stunned` |
| 🧐 | `skeptical` | `doubtful`, `suspicious`, `unconvinced` |
| 😲 | `surprised` | `startled`, `taken aback` |
| 💭 | `thoughtful` | `contemplative`, `musing`, `reflective` |

### `physical` — what your body is doing (15 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 🤕 | `achy` | `bruised`, `hurting`, `in pain` |
| 🧼 | `clean` | `showered`, `spotless` |
| 🥶 | `cold` | `chilly`, `freezing`, `shivering` |
| 😵‍💫 | `dizzy` | `lightheaded`, `woozy` |
| 😋 | `full` | `satiated`, `stuffed` |
| 💚 | `healthy` | `fit`, `robust`, `well` |
| 🥵 | `hot` | `boiling`, `overheated`, `sweltering` |
| 🍽️ | `hungry` | `peckish`, `ravenous`, `starving` |
| 🤮 | `nauseous` | `queasy`, `sick to my stomach` |
| 🤒 | `sick` | `ill`, `poorly`, `under the weather`, `unwell` |
| 🩹 | `sore` | `stiff`, `tender muscles` |
| 🦾 | `strong` | `mighty`, `powerful` |
| 💦 | `sweaty` | `clammy` |
| 🥤 | `thirsty` | `dehydrated`, `parched` |
| 🫨 | `weak` | `feeble`, `frail`, `shaky` |

### `playful` — being a menace (13 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 🧗 | `adventurous` | `daring`, `explorative`, `intrepid` |
| 😜 | `cheeky` | `irreverent`, `sassy`, `saucy` |
| 😎 | `cool` | `chill`, `slick`, `suave` |
| 🎭 | `dramatic` | `extra`, `over the top`, `theatrical` |
| 🤡 | `goofy` | `clownish`, `ridiculous` |
| 😈 | `mischievous` | `devious`, `impish`, `naughty`, `troublemaking` |
| 🤓 | `nerdy` | `bookish`, `geeky` |
| 🤘 | `rebellious` | `contrary`, `defiant`, `punk` |
| 🙃 | `sarcastic` | `dry`, `ironic`, `snarky`, `wry` |
| 🤪 | `silly` | `absurd`, `daft`, `goofball`, `zany` |
| 😏 | `smug` | `cocky`, `self satisfied` |
| 😝 | `teasing` | `joking`, `kidding`, `mocking` |
| 🤠 | `wild` | `feral`, `reckless`, `untamed` |

### `neutral` — level, in-between states (15 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| ⚖️ | `balanced` | `even keeled`, `grounded`, `steady` |
| 😶 | `blank` | `expressionless`, `nothing`, `vacant` |
| 🐝 | `busy` | `occupied`, `slammed`, `swamped with work` |
| 😌 | `calm` | `composed`, `relaxed`, `settled`, `tranquil` |
| 🚧 | `cautious` | `careful`, `hesitant`, `wary` |
| 🫰 | `indifferent` | `apathetic`, `unbothered`, `uncaring` |
| 😐 | `meh` | `mid`, `so so`, `whatever` |
| 🍃 | `mellow` | `easygoing`, `laid back`, `subdued` |
| 📻 | `nostalgic` | `homesick for the past`, `reminiscent`, `sentimental` |
| 👍 | `okay` | `alright`, `decent`, `fine` |
| ⏳ | `patient` | `enduring`, `tolerant` |
| ☮️ | `peaceful` | `harmonious`, `still` |
| 🌙 | `pensive` | `brooding`, `moody` |
| 🤫 | `quiet` | `hushed`, `silent` |
| 🕊️ | `serene` | `placid`, `untroubled` |

---

## ➕ Adding your own moods

Everything lives in [`moodemoji/data.py`](moodemoji/data.py) in two plain dictionaries — no clever machinery to learn.

To add a **new mood**, put one entry in the category it belongs to:

```python
MOOD_CATEGORIES = {
    "positive": {
        "happy": "😊",
        "smug about my code": "🧑‍💻",   # <- your new mood
        ...
```

To add a **synonym** for a mood that already exists, add one entry to `ALIASES`:

```python
ALIASES = {
    "chuffed": "delighted",
    "buzzed": "excited",   # <- your new synonym
    ...
```

Both are picked up automatically by every function in the library. Four rules are checked by the test suite, so run `pytest` after editing:

- No two core moods share an emoji (if they'd collide, make one a synonym of the other)
- Every synonym points at a mood that actually exists
- A word is either a core mood or a synonym, never both
- Words are written in tidy form already: lowercase, no punctuation, single spaces

---

## 🧪 Running the tests

```bash
pip install -e .   # required first — the tests import the installed package
pytest             # runs the whole suite
```

To run a single test:

```bash
pytest tests/test_core.py::test_mood_to_emoji
```

---

## 📜 License

MIT © Vedanta Barooah
