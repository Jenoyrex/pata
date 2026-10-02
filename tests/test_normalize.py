from pata.normalize import name_key


def test_latin_punctuation_and_case():
    assert name_key("  Rampur-Kalan  B.O. ") == "rampur kalan b o"


def test_indic_combining_marks_are_kept():
    assert name_key("राम नगर") == "राम नगर"
    assert name_key("तिरुवनंतपुरम्") == "तिरुवनंतपुरम्"


def test_zero_width_joiner_does_not_split_words():
    assert name_key("ക‍ല") == "കല"


def test_compatibility_forms_fold():
    assert name_key("ＡＢＣ") == "abc"
