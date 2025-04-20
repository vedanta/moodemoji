# 🎭 moodemoji

**moodemoji** is a playful Python library that maps your mood to the perfect emoji.  
Built as a way to learn Python packaging, it's simple, testable, and fun.

---

## 🚀 Features

- `mood_to_emoji("happy")` → 😊
- Class-based API with `MoodInterpreter`
- Built-in fallback for unknown moods
- Easily extendable

---

## 📦 Installation

Install locally (for development):

```bash
pip install -e .
```

---

## 🧑‍💻 Usage

### Functional API

```python
from moodemoji import mood_to_emoji

print(mood_to_emoji("tired"))   # 😴
print(mood_to_emoji("curious")) # 🤔
```

### Object-Oriented API

```python
from moodemoji import MoodInterpreter

mi = MoodInterpreter("excited")
print(mi.get_emoji())        # 🤩
mi.set_mood("sad")
print(mi.get_emoji())        # 😢
```

---

## ✅ Supported Moods

- happy
- sad
- angry
- excited
- tired
- love
- confused

---

## 📁 Project Structure

```
moodemoji/
├── moodemoji/         # Library code
│   ├── __init__.py
│   └── core.py
├── tests/             # Unit tests
├── pyproject.toml     # Packaging config
└── README.md
```

---

## 🧪 Run Tests

```bash
pytest
```

---

## 📜 License

MIT © Vedanta Barooah
