# 🎭 moodemoji

**Give it a mood, get an emoji back.**

```python
>>> from moodemoji import mood_to_emoji
>>> mood_to_emoji("happy")
'😊'
```

That's the whole idea. `moodemoji` knows **1,304 mood words** — 370 core moods plus 934 synonyms — and maps each one to a fitting emoji. It has no dependencies, needs no setup, and never raises on unknown input.

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

With no arguments, returns all 370 core mood names, alphabetically sorted:

```python
from moodemoji import list_moods

list_moods()           # ['absurd', 'accepting', 'achy', ...]
len(list_moods())      # 370
```

Pass a category name to narrow it down:

```python
list_moods("positive")   # ['admiring', 'aesthetic', 'amused', ...]
len(list_moods("positive"))  # 48
```

If you pass a category that doesn't exist, you get a helpful `ValueError` rather than a silent empty list:

```python
list_moods("vibes")
# ValueError: unknown category 'vibes'; expected one of:
#   cognitive, energy, existential, negative, neutral, physical, playful, positive, slang, social
```

#### `list_categories()` — the ten mood families

```python
from moodemoji import list_categories

list_categories()
# ['cognitive', 'energy', 'existential', 'negative', 'neutral',
#  'physical', 'playful', 'positive', 'slang', 'social']
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

len(list_moods())       # 370  core moods
len(list_all_terms())   # 1304  core moods + synonyms
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

<!-- BEGIN GENERATED: mood tables — edit moodemoji/data.py, then run tools/build_docs.py -->

### `positive` — feeling good (48 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 👏 | `admiring` | `admiration`, `impressed`, `in admiration` |
| 🖼️ | `aesthetic` | `aesthetically pleased`, `moved by beauty` |
| 😆 | `amused` | `entertained`, `tickled` |
| ⏰ | `anticipating` | `anticipation`, `counting down`, `expecting`, `looking forward` |
| 🌟 | `awestruck` | `in awe`, `wonderstruck` |
| 😇 | `blissful` | `heavenly`, `serene bliss` |
| 🥹 | `charmed` | `beguiled`, `enchanted`, `won over` |
| 😃 | `cheerful` | `bright`, `chipper`, `upbeat` |
| 💯 | `confident` | `assured`, `bold`, `self assured` |
| 🙂 | `content` | `at peace`, `comfortable`, `cosy`, `cozy`, … |
| 🦁 | `courageous` | `brave`, `fearless`, `gutsy`, `valiant` |
| 🤤 | `craving` | `hankering`, `hungry for` |
| 😁 | `delighted` | `chuffed` |
| 🦸 | `empowered` | `agency`, `capable`, `in control` |
| 🌠 | `entranced` | `captivated`, `mesmerized`, `spellbound`, `transfixed` |
| 🎆 | `euphoric` | `elevated`, `smitten with life` |
| 🤩 | `excited` | `cant wait`, `champing at the bit`, `eager`, `enthusiastic`, … |
| 🎉 | `festive` | `celebratory`, `party` |
| 🌺 | `flattered` | `complimented` |
| 🪁 | `free` | `footloose`, `untethered` |
| 🎁 | `generous` | `charitable`, `giving`, `openhanded` |
| 🤭 | `giddy` | `giggly` |
| 🙏 | `grateful` | `appreciative`, `blessed`, `much obliged`, `thankful` |
| 😊 | `happy` | `buoyant`, `dandy`, `glad`, `good`, … |
| 🌱 | `hopeful` | `encouraged`, `expectant`, `fingers crossed` |
| 🙇 | `humble` | `modest`, `unassuming` |
| 💡 | `inspired` | `creative spark` |
| 🔍 | `interested` | `engaged`, `interest`, `keen` |
| 😄 | `joyful` | `elated`, `gleeful`, `jubilant`, `merry`, … |
| 🪽 | `liberated` | `unchained`, `unshackled` |
| 🍀 | `lucky` | `fortunate` |
| 🔥 | `motivated` | `ambitious`, `driven`, `fired up`, `focused fire` |
| 🌈 | `optimistic` | `positive` |
| 🦚 | `proud` | `accomplished`, `dignified`, `pleased with myself` |
| ✨ | `radiant` | `beaming`, `glowing` |
| 😮‍💨 | `relieved` | `reassured`, `unburdened`, `weight off my shoulders` |
| 📿 | `reverent` | `devout`, `worshipful` |
| 🌹 | `romantic` | `amorous`, `lovey dovey` |
| 🏠 | `safe` | `out of danger`, `protected`, `sheltered` |
| 👌 | `satisfied` | `gratified` |
| 🔒 | `secure` | `on solid ground`, `stable` |
| 🔮 | `spiritual` | `mystical`, `soulful` |
| 🥇 | `successful` | `achieved`, `winning big` |
| 🎢 | `thrilled` | `exhilarated` |
| 🏆 | `triumphant` | `victorious`, `winning` |
| ✅ | `validated` | `acknowledged`, `affirmed` |
| ⚔️ | `vindicated` | `justified`, `proven right` |
| 🧸 | `wholesome` | `heartwarming`, `sweet` |

### `negative` — feeling bad (72 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 😠 | `angry` | `cross`, `heated`, `hot under the collar`, `mad`, … |
| 😤 | `annoyed` | `bothered`, `miffed`, `peeved` |
| 😰 | `anxious` | `apprehensive`, `jittery`, `nervous`, `on edge`, … |
| 🙈 | `ashamed` | `humiliated`, `mortified`, `sheepish` |
| 🗡️ | `betrayed` | `double crossed`, `stabbed in the back` |
| 🍋 | `bitter` | `cynical`, `jaded`, `sour` |
| 💸 | `broke` | `penniless`, `skint`, `strapped` |
| 🎒 | `burdened` | `carrying a lot`, `weighed down` |
| 🎲 | `cheated` | `conned`, `ripped off`, `scammed`, `swindled` |
| 🧱 | `claustrophobic` | `walls closing in` |
| 😒 | `contemptuous` | `contempt`, `disdainful`, `scornful`, `sneering` |
| 🕷️ | `creeped out` | `creeped`, `skeeved`, `unnerved` |
| 🏳️ | `defeated` | `beaten`, `demoralized`, `resigned` |
| 😔 | `depressed` | `despondent`, `low` |
| 😞 | `disappointed` | `disheartened`, `gutted`, `let down` |
| 🤢 | `disgusted` | `grossed out`, `repulsed`, `revolted` |
| 🪞 | `disillusioned` | `disenchanted`, `let down by life` |
| 👎 | `disrespected` | `belittled`, `dismissed`, `talked down to` |
| 🚨 | `distrustful` | `on guard`, `wary of others` |
| 🌘 | `dreading` | `dread`, `foreboding`, `impending doom` |
| 🫤 | `envious` | `covetous` |
| 📦 | `forgotten` | `left behind`, `out of sight` |
| 🥚 | `fragile` | `breakable`, `brittle`, `delicate` |
| 😣 | `frustrated` | `annoyed at everything`, `exasperated`, `fed up` |
| 🤬 | `furious` | `enraged`, `irate`, `livid`, `seething` |
| 🌧️ | `gloomy` | `dreary`, `grey`, `overcast` |
| 🥀 | `grieving` | `bereaved`, `heartsore`, `mourning` |
| 😓 | `guilty` | `remorseful`, `sorry` |
| 🖤 | `hateful` | `full of hate`, `loathing` |
| 💔 | `heartbroken` | `broken hearted`, `crushed`, `hurt`, `lovesick` |
| 🕳️ | `hopeless` | `despairing`, `helpless`, `lost` |
| 😧 | `horrified` | `aghast`, `appalled` |
| 🔇 | `ignored` | `talked over`, `unacknowledged` |
| 🫥 | `insecure` | `inadequate`, `self conscious`, `unsure of myself` |
| 🫧 | `invisible` | `overlooked`, `unnoticed` |
| 😖 | `irritated` | `agitated`, `cranky`, `grumpy`, `irked` |
| 🐍 | `jealous` | — |
| 🌊 | `longing` | `aching for`, `pining` |
| 😩 | `miserable` | `awful`, `terrible`, `wretched` |
| 🗯️ | `misunderstood` | `not understood`, `taken the wrong way` |
| 🍂 | `neglected` | `unattended`, `uncared for` |
| 🫠 | `numb` | `detached`, `dissociated`, `empty`, `hollow` |
| 😑 | `offended` | `affronted`, `insulted` |
| 💢 | `outraged` | `indignant`, `scandalized`, `up in arms` |
| 😵 | `overwhelmed` | `buried`, `flooded`, `swamped`, `too much going on` |
| 😳 | `panicked` | `alarmed`, `frantic`, `freaking out` |
| 👁️ | `paranoid` | `conspiratorial`, `paranoia`, `watched` |
| ☁️ | `pessimistic` | `downbeat`, `glass half empty` |
| 🫵 | `petty` | `nitpicky`, `small minded` |
| 🔐 | `possessive` | `clingy`, `territorial` |
| 🗜️ | `pressured` | `on the spot`, `squeezed` |
| 😥 | `regretful` | `rueful`, `wistful` |
| 🚫 | `rejected` | `knocked back`, `spurned`, `turned down` |
| 🔁 | `replaceable` | `expendable`, `just a number` |
| 😾 | `resentful` | `begrudging`, `spiteful` |
| 😢 | `sad` | `blue`, `crestfallen`, `dejected`, `down`, … |
| 🌅 | `saudade` | `bittersweet`, `sweet sorrow` |
| 😨 | `scared` | `afraid`, `fearful`, `frightened`, `quaking`, … |
| 🕸️ | `self loathing` | `self disgust`, `self hatred` |
| 🌩️ | `stormy` | `tempestuous`, `turbulent` |
| 😫 | `stressed` | `strained`, `tense`, `under pressure` |
| 🫁 | `suffocated` | `cant breathe`, `smothered` |
| 😱 | `terrified` | `horror struck`, `petrified` |
| ⛓️ | `tormented` | `in torment`, `tortured` |
| 🪤 | `trapped` | `boxed in`, `cornered`, `no way out` |
| 💥 | `traumatized` | `scarred`, `shell shocked` |
| 🌚 | `unlucky` | `cursed`, `hard luck`, `jinxed` |
| 📉 | `unworthy` | `not good enough`, `undeserving`, `worthless` |
| 😡 | `vengeful` | `out for revenge`, `revengeful`, `vindictive` |
| 🫗 | `vulnerable` | `exposed`, `unguarded`, `wide open` |
| 😟 | `worried` | `concerned`, `troubled` |
| 🧲 | `yearning` | `craving deeply`, `hungering` |

### `energy` — how much gas is in the tank (29 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 👀 | `alert` | `attentive`, `awake`, `sharp` |
| 🔊 | `amped` | `amped up`, `juiced` |
| 🕯️ | `burnt out` | `burned out`, `burnout`, `crispy`, `fried` |
| 🛬 | `crashing` | `coming down`, `energy crash` |
| 🪫 | `drained` | `depleted`, `running on empty` |
| ⚡ | `energized` | `charged`, `lively`, `peppy`, `vigorous` |
| 😪 | `exhausted` | `knackered`, `shattered`, `spent`, `wiped` |
| 🥴 | `groggy` | `foggy headed`, `just woke up` |
| 🍺 | `hungover` | `rough morning`, `the fear` |
| 🚀 | `hyper` | `bouncing`, `manic` |
| ✈️ | `jetlagged` | `jet lag`, `time zoned` |
| 🦥 | `lazy` | `idle`, `listless`, `unmotivated` |
| 🛏️ | `napping` | `having a lie down`, `nap time` |
| 🏭 | `overworked` | `grinding`, `worked to the bone` |
| 🔌 | `recharging` | `plugging in`, `topping up` |
| 🚿 | `refreshed` | `rejuvenated`, `renewed`, `revitalized` |
| 🛌 | `rested` | `fresh`, `restored` |
| 🌀 | `restless` | `antsy`, `fidgety`, `unsettled` |
| 🏎️ | `revved` | `engine running`, `revved up` |
| 🔄 | `second wind` | `back at it`, `found my energy` |
| 🌃 | `sleep deprived` | `no sleep`, `running on fumes` |
| 💤 | `sleepy` | `dozy`, `drowsy` |
| 🐌 | `sluggish` | `heavy`, `slow` |
| 😴 | `tired` | `beat`, `dead on my feet`, `fatigued`, `running low`, … |
| 🌋 | `unstoppable` | `full send`, `on a roll` |
| 🌞 | `wide awake` | `cant sleep`, `eyes wide open` |
| 💨 | `winded` | `out of breath`, `puffed` |
| ☕ | `wired` | `buzzing`, `caffeinated` |
| 📺 | `zoned out` | `checked out`, `vacant stare` |

### `social` — feelings about other people (37 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 😘 | `affectionate` | `cuddly`, `tender`, `warm` |
| 🥲 | `apologetic` | `contrite`, `saying sorry` |
| 💐 | `appreciated` | `seen`, `valued` |
| 😬 | `awkward` | `cringey`, `out of place`, `uncomfortable` |
| 🧩 | `belonging` | `at home with them`, `part of something` |
| 🤲 | `compassionate` | `compassion`, `merciful`, `tenderhearted` |
| 🔗 | `connected` | `in sync`, `on the same wavelength` |
| 💘 | `crush` | `butterflies`, `crushing` |
| 💋 | `desire` | `attracted`, `wanting` |
| 💍 | `devoted` | `committed`, `loyal` |
| ⛓️‍💥 | `disconnected` | `drifted apart`, `out of touch` |
| 😅 | `embarrassed` | `flustered`, `red faced`, `want the ground to swallow me` |
| 💞 | `empathetic` | `empathic`, `empathy`, `feeling with you` |
| 🚪 | `estranged` | `cut off`, `no contact` |
| 😉 | `flirty` | `coy`, `playful wink` |
| 🙌 | `forgiven` | `absolved`, `off the hook` |
| 🤍 | `forgiving` | `letting it go`, `no hard feelings` |
| 🤝 | `friendly` | `amiable`, `kind`, `sociable` |
| 👂 | `heard` | `listened to`, `properly understood` |
| 🎟️ | `included` | `brought in`, `invited` |
| 💓 | `infatuated` | `head over heels`, `obsessed with them` |
| 🐚 | `introverted` | `inward`, `withdrawn` |
| 🥺 | `lonely` | `abandoned`, `alone`, `homesick`, `isolated`, … |
| ❤️ | `love` | `adoring`, `besotted`, `in love`, `loving`, … |
| 🥰 | `loved` | `adored`, `cherished`, `wanted` |
| 🍼 | `nurturing` | `caring for`, `looking after` |
| 🗣️ | `outgoing` | `chatty`, `extroverted`, `gregarious` |
| 😿 | `pity` | `feel bad for them`, `pitying` |
| 📣 | `popular` | `everyones favourite`, `in demand` |
| 🛡️ | `protective` | `defensive`, `guarded` |
| 🎖️ | `respected` | `held in regard`, `looked up to` |
| 🫣 | `shy` | `bashful`, `reserved`, `timid` |
| 🫂 | `supported` | `backed up`, `cared for`, `held` |
| 🫶 | `sympathetic` | `commiserating`, `sympathy` |
| 🤞 | `trusting` | `hopeful in others`, `trustful` |
| 🔕 | `unheard` | `not listened to`, `talking to a wall` |
| 👋 | `welcoming` | `hospitable` |

### `cognitive` — what your brain is doing (44 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 🤯 | `amazed` | `astonished`, `dumbfounded`, `mind blown` |
| 📊 | `analytical` | `analysing`, `breaking it down` |
| ⛔ | `blocked` | `creatively blocked`, `writers block` |
| 🥱 | `bored` | `restive`, `tedious`, `twiddling my thumbs`, `understimulated` |
| 🧠 | `brainstorming` | `ideating`, `spitballing` |
| 🧮 | `calculating` | `running the numbers`, `scheming` |
| ☑️ | `certain` | `no doubt`, `sure` |
| 📕 | `closed minded` | `not budging`, `set in my ways` |
| 🤷 | `clueless` | `bewildered`, `lost the plot`, `no idea` |
| 😕 | `confused` | `at sea`, `baffled`, `disoriented`, `lost the thread`, … |
| ✍️ | `convinced` | `persuaded`, `sold on it` |
| 🎨 | `creative` | `artistic`, `imaginative`, `inventive` |
| 🤔 | `curious` | `inquisitive`, `intrigued`, `nosy`, `want to know more`, … |
| 🌤️ | `daydreaming` | `head in the clouds`, `off in a dream` |
| 🔨 | `decisive` | `made up my mind`, `resolved to act` |
| 💪 | `determined` | `not giving up`, `persistent`, `resolute`, `stubborn`, … |
| 🦋 | `distracted` | `scattered`, `spacey`, `unfocused` |
| 🧘 | `enlightened` | `awakened`, `centered`, `mindful` |
| 🎇 | `eureka` | `aha`, `it clicked`, `lightbulb moment` |
| 🎯 | `focused` | `absorbed`, `concentrated`, `dialed in`, `heads down`, … |
| 🌫️ | `forgetful` | `absent minded`, `foggy` |
| 🏄 | `in the zone` | `flow`, `flow state` |
| 🤨 | `indecisive` | `conflicted`, `on the fence`, `torn` |
| 🧑‍⚖️ | `judgmental` | `critical of everyone`, `judging` |
| 🎓 | `learning` | `in training`, `picking it up` |
| ➗ | `logical` | `rational`, `reasoned` |
| 📐 | `meticulous` | `detail obsessed`, `perfectionist`, `precise` |
| 🐣 | `naive` | `green`, `innocent`, `wet behind the ears` |
| 🔭 | `observant` | `taking it in`, `watching closely` |
| 🌐 | `open minded` | `receptive`, `willing to hear it` |
| 🌪️ | `overthinking` | `in my head`, `ruminating`, `spiraling` |
| 🏛️ | `philosophical` | `waxing philosophical` |
| 🗺️ | `planning` | `mapping it out`, `plotting` |
| 📜 | `poetic` | `lyrical`, `waxing poetic` |
| 🐢 | `procrastinating` | `avoiding it`, `putting it off` |
| 😮 | `shocked` | `floored`, `speechless`, `stunned` |
| 🧐 | `skeptical` | `doubtful`, `suspicious`, `unconvinced` |
| ♟️ | `strategic` | `playing chess`, `thinking ahead` |
| 🪨 | `stuck` | `hit a wall`, `no progress` |
| 📚 | `studious` | `hitting the books`, `swotting` |
| 😲 | `surprised` | `startled`, `taken aback` |
| 💭 | `thoughtful` | `contemplative`, `musing`, `reflective` |
| ❓ | `uncertain` | `not sure`, `unsure`, `up in the air` |
| 🦉 | `wise` | `sage`, `worldly` |

### `physical` — what your body is doing (34 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 🤕 | `achy` | `bruised`, `hurting`, `in pain` |
| 🤧 | `allergic` | `allergies`, `sneezy` |
| 🎈 | `bloated` | `food baby`, `puffy` |
| 🌬️ | `breathless` | `gasping`, `lungs burning` |
| 🧼 | `clean` | `showered`, `spotless` |
| 🤸 | `clumsy` | `butterfingers`, `tripping over myself` |
| 🥶 | `cold` | `chilly`, `freezing`, `shivering` |
| 😷 | `congested` | `blocked up`, `stuffy nose` |
| 🪣 | `dirty` | `grimy`, `grubby`, `need a shower` |
| 😵‍💫 | `dizzy` | `lightheaded`, `woozy` |
| 🍻 | `drunk` | `hammered`, `sloshed`, `wasted` |
| 🌡️ | `feverish` | `burning up`, `running a temperature` |
| 🧊 | `frozen` | `icy`, `numb with cold` |
| 😋 | `full` | `satiated`, `stuffed` |
| 🩰 | `graceful` | `elegant`, `poised` |
| 🍔 | `hangry` | `hungry and angry`, `need food now` |
| 💚 | `healthy` | `fit`, `robust`, `well` |
| 🥵 | `hot` | `boiling`, `overheated`, `sweltering` |
| 🍽️ | `hungry` | `could eat a horse`, `peckish`, `ravenous`, `starving` |
| 🐜 | `itchy` | `prickly`, `scratchy` |
| 🤮 | `nauseous` | `queasy`, `sick to my stomach` |
| 📳 | `overstimulated` | `sensory overload`, `too much input` |
| 💅 | `pampered` | `spoiled`, `treated` |
| 🩼 | `recovering` | `healing`, `on the mend` |
| 🤒 | `sick` | `ill`, `poorly`, `under the weather`, `unwell` |
| 🚰 | `sober` | `clear headed`, `not drinking` |
| 🩹 | `sore` | `stiff`, `tender muscles` |
| 🦾 | `strong` | `mighty`, `powerful` |
| 🔆 | `sunburnt` | `burnt by the sun`, `lobster` |
| 💦 | `sweaty` | `clammy` |
| 🥤 | `thirsty` | `dehydrated`, `parched` |
| ✳️ | `tingly` | `buzzy skin`, `pins and needles` |
| 🥂 | `tipsy` | `lightly drunk`, `one too many` |
| 🫨 | `weak` | `feeble`, `frail`, `shaky` |

### `playful` — being a menace (32 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 🧗 | `adventurous` | `daring`, `explorative`, `intrepid` |
| 📸 | `attention seeking` | `look at me`, `main stage` |
| 📢 | `boastful` | `big talk`, `bragging` |
| 🏖️ | `carefree` | `breezy`, `without a care` |
| 🃏 | `chaotic` | `chaos`, `gremlin energy` |
| 😜 | `cheeky` | `irreverent`, `sassy`, `saucy` |
| 🔑 | `clever` | `crafty`, `smart` |
| 🥊 | `competitive` | `in it to win it`, `must win` |
| 😎 | `cool` | `chill`, `slick`, `suave` |
| 💃 | `dancing` | `dancey`, `moving to it` |
| 🎭 | `dramatic` | `extra`, `over the top`, `theatrical` |
| 🎮 | `gamer` | `gaming`, `one more round` |
| 👺 | `goblin mode` | `feral mode`, `goblin` |
| 🤡 | `goofy` | `clownish`, `ridiculous` |
| 😈 | `mischievous` | `devious`, `impish`, `naughty`, `troublemaking` |
| 🎵 | `musical` | `humming along`, `in the music` |
| 🤓 | `nerdy` | `bookish`, `geeky` |
| 🤘 | `rebellious` | `contrary`, `defiant`, `punk` |
| 🥁 | `rowdy` | `boisterous`, `raucous` |
| 🙃 | `sarcastic` | `dry`, `ironic`, `snarky`, `wry` |
| 🕺 | `showing off` | `peacocking`, `performing` |
| 🤪 | `silly` | `daft`, `goofball`, `in a silly mood`, `zany` |
| 🪿 | `silly goose` | `absolute goose`, `goose` |
| 🎤 | `singing` | `belting it out`, `sing song` |
| 😏 | `smug` | `cocky`, `self satisfied` |
| 🪩 | `spontaneous` | `no plan`, `on a whim` |
| 🏀 | `sporty` | `athletic`, `game on` |
| 😝 | `teasing` | `joking`, `kidding`, `mocking` |
| 🎡 | `unhinged` | `no thoughts`, `off the rails` |
| 🦄 | `whimsical` | `fanciful`, `twee` |
| 🤠 | `wild` | `feral`, `reckless`, `untamed` |
| ✏️ | `witty` | `quick witted`, `sharp tongued` |

### `neutral` — level, in-between states (30 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 🍵 | `accepting` | `at peace with it`, `come to terms` |
| ⚖️ | `balanced` | `even keeled`, `grounded`, `steady` |
| 😶 | `blank` | `expressionless`, `nothing`, `vacant` |
| 🐝 | `busy` | `occupied`, `slammed`, `swamped with work` |
| 😌 | `calm` | `composed`, `cool as a cucumber`, `relaxed`, `settled`, … |
| 👕 | `casual` | `dressed down`, `relaxed dress` |
| 🚧 | `cautious` | `careful`, `hesitant`, `wary` |
| 🐓 | `early` | `ahead of time`, `too early` |
| 🎩 | `formal` | `black tie`, `buttoned up` |
| 🫰 | `indifferent` | `apathetic`, `unbothered`, `uncaring` |
| 🕐 | `late` | `behind schedule`, `running late` |
| 😐 | `meh` | `mid`, `so so`, `whatever` |
| 🍃 | `mellow` | `easygoing`, `laid back`, `subdued` |
| 🧺 | `messy` | `all over the place`, `disorganized` |
| 📻 | `nostalgic` | `back in the day`, `homesick for the past`, `reminiscent`, `sentimental` |
| 👍 | `okay` | `alright`, `decent`, `fine` |
| 🗂️ | `organized` | `in order`, `sorted`, `tidy` |
| ⏳ | `patient` | `enduring`, `tolerant` |
| ☮️ | `peaceful` | `harmonious`, `still` |
| 🌙 | `pensive` | `brooding`, `moody` |
| 🧭 | `prepared` | `ready`, `set up` |
| 🧿 | `present` | `here now`, `in the moment` |
| 📈 | `productive` | `getting things done`, `on a streak` |
| 💼 | `professional` | `business mode`, `work mode` |
| 🤫 | `quiet` | `hushed`, `silent` |
| 📅 | `routine` | `on autopilot`, `same as always` |
| 🏃 | `rushed` | `in a hurry`, `no time` |
| 🕊️ | `serene` | `placid`, `untroubled` |
| 🗿 | `stoic` | `taking it on the chin`, `unmoved` |
| 🎰 | `unprepared` | `not ready`, `winging it` |

### `slang` — internet and modern shorthand (28 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 🆒 | `based` | `true to myself`, `unbothered by opinions` |
| 📹 | `caught in 4k` | `busted`, `caught red handed` |
| 🍳 | `cooked` | `done for`, `im cooked` |
| 🙊 | `cringe` | `cringing`, `second hand embarrassment` |
| 🛸 | `delulu` | `delusional`, `living a fantasy` |
| 📱 | `doomscrolling` | `doomscroll`, `scrolling the void` |
| 🪐 | `era` | `in my era`, `new chapter` |
| 💎 | `flexing` | `flex`, `showing it off` |
| 📲 | `fomo` | `fear of missing out`, `missing out` |
| 👻 | `ghosted` | `ghost`, `left on read` |
| ⬆️ | `glow up` | `glowed up`, `transformation` |
| 🐐 | `goated` | `goat`, `greatest of all time` |
| 🤐 | `iykyk` | `if you know you know`, `inside joke` |
| 🏝️ | `jomo` | `happily missing out`, `joy of missing out` |
| 🏘️ | `living rent free` | `cant stop thinking about it`, `rent free` |
| 🔉 | `lowkey` | `low key`, `quietly` |
| 🎬 | `main character` | `main character energy`, `protagonist` |
| 📛 | `menty b` | `meltdown`, `mental breakdown` |
| 🤖 | `npc` | `background character`, `npc energy` |
| 😽 | `rizz` | `charisma`, `smooth talker` |
| 🧂 | `salty` | `bitter about it`, `sour grapes` |
| 🫢 | `shook` | `rattled`, `shaken` |
| 👑 | `slay` | `killing it`, `slaying` |
| 🌸 | `soft launch` | `hinting at it`, `soft launching` |
| 🕵️ | `sus` | `something is off`, `suspect` |
| 🌿 | `touch grass` | `need to go outside`, `terminally online` |
| 🎧 | `vibing` | `good vibes`, `in my element`, `vibe` |
| 🧽 | `washed` | `over the hill`, `past my prime` |

### `existential` — the big questions (16 moods)

| Emoji | Mood | Also accepts |
|:---:|---|---|
| 🎪 | `absurd` | `absurdist`, `cosmic joke` |
| 🌑 | `existential` | `existential dread`, `staring into the void` |
| ⏱️ | `impermanence` | `nothing lasts`, `this too shall pass` |
| 🌌 | `insignificant` | `a speck`, `tiny in the universe` |
| 🏍️ | `midlife crisis` | `crisis of meaning`, `midlife` |
| 💀 | `mortal` | `aware of death`, `memento mori` |
| ⚫ | `nihilistic` | `nihilism`, `nothing matters` |
| ♾️ | `oneness` | `at one`, `connected to everything` |
| 🥾 | `pilgrim` | `on a journey`, `pilgrimage` |
| ⛰️ | `purposeful` | `on a mission`, `sense of purpose` |
| ❔ | `questioning` | `questioning everything`, `why are we here` |
| 🌄 | `reborn` | `born again`, `fresh start`, `new beginning` |
| 🔦 | `searching` | `looking for meaning`, `seeking` |
| 🏔️ | `solitude` | `alone by choice`, `happy alone` |
| 🧎 | `surrendered` | `letting go entirely`, `surrender` |
| 🕉️ | `transcendent` | `beyond myself`, `transcendence` |

<!-- END GENERATED: mood tables -->

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
