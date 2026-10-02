"""Script-agnostic text normalization.

Deliberately conservative: no abbreviation expansion, no transliteration, no
spelling correction. Those change meaning and must be measured, not assumed.
"""

import unicodedata


def name_key(text: str) -> str:
    """Comparison key for names: NFKC, casefolded, punctuation/symbols/spaces collapsed.

    Combining marks (Indic vowel signs, viramas) are kept, so native-script names
    stay intact. Format characters such as ZWJ/ZWNJ are dropped without splitting
    the word.
    """
    out = []
    for ch in unicodedata.normalize("NFKC", text).casefold():
        cat = unicodedata.category(ch)
        if cat == "Cf":
            continue
        out.append(" " if cat[0] in "PSZ" or cat == "Cc" else ch)
    return " ".join("".join(out).split())
