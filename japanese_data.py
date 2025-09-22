"""
База данных японских символов для викторин
"""

# Кандзи (иероглифы)
KANJI_DATA = {
    "水": {
        "meaning": "вода",
        "reading": "みず",
        "romaji": "mizu"
    },
    "火": {
        "meaning": "огонь",
        "reading": "ひ",
        "romaji": "hi"
    },
    "木": {
        "meaning": "дерево",
        "reading": "き",
        "romaji": "ki"
    },
    "金": {
        "meaning": "золото, металл",
        "reading": "きん",
        "romaji": "kin"
    },
    "土": {
        "meaning": "земля",
        "reading": "つち",
        "romaji": "tsuchi"
    },
    "人": {
        "meaning": "человек",
        "reading": "ひと",
        "romaji": "hito"
    },
    "日": {
        "meaning": "солнце, день",
        "reading": "ひ",
        "romaji": "hi"
    },
    "月": {
        "meaning": "луна, месяц",
        "reading": "つき",
        "romaji": "tsuki"
    },
    "山": {
        "meaning": "гора",
        "reading": "やま",
        "romaji": "yama"
    },
    "川": {
        "meaning": "река",
        "reading": "かわ",
        "romaji": "kawa"
    },
    "大": {
        "meaning": "большой",
        "reading": "おおきい",
        "romaji": "ookii"
    },
    "小": {
        "meaning": "маленький",
        "reading": "ちいさい",
        "romaji": "chiisai"
    }
}

# Хирагана (основная слоговая азбука) - полная таблица
HIRAGANA_DATA = {
    # Основные гласные
    "あ": {"romaji": "a", "sound": "а"},
    "い": {"romaji": "i", "sound": "и"},
    "う": {"romaji": "u", "sound": "у"},
    "え": {"romaji": "e", "sound": "э"},
    "お": {"romaji": "o", "sound": "о"},
    
    # K-ряд
    "か": {"romaji": "ka", "sound": "ка"},
    "き": {"romaji": "ki", "sound": "ки"},
    "く": {"romaji": "ku", "sound": "ку"},
    "け": {"romaji": "ke", "sound": "кэ"},
    "こ": {"romaji": "ko", "sound": "ко"},
    
    # S-ряд
    "さ": {"romaji": "sa", "sound": "са"},
    "し": {"romaji": "shi", "sound": "си"},
    "す": {"romaji": "su", "sound": "су"},
    "せ": {"romaji": "se", "sound": "сэ"},
    "そ": {"romaji": "so", "sound": "со"},
    
    # T-ряд
    "た": {"romaji": "ta", "sound": "та"},
    "ち": {"romaji": "chi", "sound": "ти"},
    "つ": {"romaji": "tsu", "sound": "цу"},
    "て": {"romaji": "te", "sound": "тэ"},
    "と": {"romaji": "to", "sound": "то"},
    
    # N-ряд
    "な": {"romaji": "na", "sound": "на"},
    "に": {"romaji": "ni", "sound": "ни"},
    "ぬ": {"romaji": "nu", "sound": "ну"},
    "ね": {"romaji": "ne", "sound": "нэ"},
    "の": {"romaji": "no", "sound": "но"},
    
    # H-ряд
    "は": {"romaji": "ha", "sound": "ха"},
    "ひ": {"romaji": "hi", "sound": "хи"},
    "ふ": {"romaji": "fu", "sound": "фу"},
    "へ": {"romaji": "he", "sound": "хэ"},
    "ほ": {"romaji": "ho", "sound": "хо"},
    
    # M-ряд
    "ま": {"romaji": "ma", "sound": "ма"},
    "み": {"romaji": "mi", "sound": "ми"},
    "む": {"romaji": "mu", "sound": "му"},
    "め": {"romaji": "me", "sound": "мэ"},
    "も": {"romaji": "mo", "sound": "мо"},
    
    # Y-ряд
    "や": {"romaji": "ya", "sound": "я"},
    "ゆ": {"romaji": "yu", "sound": "ю"},
    "よ": {"romaji": "yo", "sound": "ё"},
    
    # R-ряд
    "ら": {"romaji": "ra", "sound": "ра"},
    "り": {"romaji": "ri", "sound": "ри"},
    "る": {"romaji": "ru", "sound": "ру"},
    "れ": {"romaji": "re", "sound": "рэ"},
    "ろ": {"romaji": "ro", "sound": "ро"},
    
    # W-ряд и N
    "わ": {"romaji": "wa", "sound": "ва"},
    "を": {"romaji": "wo", "sound": "во"},
    "ん": {"romaji": "n", "sound": "н"}
}

# Хирагана с тэнтэн (濁点) и мару (半濁点)
HIRAGANA_DAKUTEN_DATA = {
    # G-ряд (с тэнтэн)
    "が": {"romaji": "ga", "sound": "га"},
    "ぎ": {"romaji": "gi", "sound": "ги"},
    "ぐ": {"romaji": "gu", "sound": "гу"},
    "げ": {"romaji": "ge", "sound": "гэ"},
    "ご": {"romaji": "go", "sound": "го"},
    
    # Z-ряд (с тэнтэн)
    "ざ": {"romaji": "za", "sound": "дза"},
    "じ": {"romaji": "ji", "sound": "дзи"},
    "ず": {"romaji": "zu", "sound": "дзу"},
    "ぜ": {"romaji": "ze", "sound": "дзэ"},
    "ぞ": {"romaji": "zo", "sound": "дзо"},
    
    # D-ряд (с тэнтэн)
    "だ": {"romaji": "da", "sound": "да"},
    "ぢ": {"romaji": "di", "sound": "ди"},
    "づ": {"romaji": "du", "sound": "ду"},
    "で": {"romaji": "de", "sound": "дэ"},
    "ど": {"romaji": "do", "sound": "до"},
    
    # B-ряд (с тэнтэн)
    "ば": {"romaji": "ba", "sound": "ба"},
    "び": {"romaji": "bi", "sound": "би"},
    "ぶ": {"romaji": "bu", "sound": "бу"},
    "べ": {"romaji": "be", "sound": "бэ"},
    "ぼ": {"romaji": "bo", "sound": "бо"},
    
    # P-ряд (с мару)
    "ぱ": {"romaji": "pa", "sound": "па"},
    "ぴ": {"romaji": "pi", "sound": "пи"},
    "ぷ": {"romaji": "pu", "sound": "пу"},
    "ぺ": {"romaji": "pe", "sound": "пэ"},
    "ぽ": {"romaji": "po", "sound": "по"}
}

# Катакана (слоговая азбука для заимствованных слов) - полная таблица
KATAKANA_DATA = {
    # Основные гласные
    "ア": {"romaji": "a", "sound": "а"},
    "イ": {"romaji": "i", "sound": "и"},
    "ウ": {"romaji": "u", "sound": "у"},
    "エ": {"romaji": "e", "sound": "э"},
    "オ": {"romaji": "o", "sound": "о"},
    
    # K-ряд
    "カ": {"romaji": "ka", "sound": "ка"},
    "キ": {"romaji": "ki", "sound": "ки"},
    "ク": {"romaji": "ku", "sound": "ку"},
    "ケ": {"romaji": "ke", "sound": "кэ"},
    "コ": {"romaji": "ko", "sound": "ко"},
    
    # S-ряд
    "サ": {"romaji": "sa", "sound": "са"},
    "シ": {"romaji": "shi", "sound": "си"},
    "ス": {"romaji": "su", "sound": "су"},
    "セ": {"romaji": "se", "sound": "сэ"},
    "ソ": {"romaji": "so", "sound": "со"},
    
    # T-ряд
    "タ": {"romaji": "ta", "sound": "та"},
    "チ": {"romaji": "chi", "sound": "ти"},
    "ツ": {"romaji": "tsu", "sound": "цу"},
    "テ": {"romaji": "te", "sound": "тэ"},
    "ト": {"romaji": "to", "sound": "то"},
    
    # N-ряд
    "ナ": {"romaji": "na", "sound": "на"},
    "ニ": {"romaji": "ni", "sound": "ни"},
    "ヌ": {"romaji": "nu", "sound": "ну"},
    "ネ": {"romaji": "ne", "sound": "нэ"},
    "ノ": {"romaji": "no", "sound": "но"},
    
    # H-ряд
    "ハ": {"romaji": "ha", "sound": "ха"},
    "ヒ": {"romaji": "hi", "sound": "хи"},
    "フ": {"romaji": "fu", "sound": "фу"},
    "ヘ": {"romaji": "he", "sound": "хэ"},
    "ホ": {"romaji": "ho", "sound": "хо"},
    
    # M-ряд
    "マ": {"romaji": "ma", "sound": "ма"},
    "ミ": {"romaji": "mi", "sound": "ми"},
    "ム": {"romaji": "mu", "sound": "му"},
    "メ": {"romaji": "me", "sound": "мэ"},
    "モ": {"romaji": "mo", "sound": "мо"},
    
    # Y-ряд
    "ヤ": {"romaji": "ya", "sound": "я"},
    "ユ": {"romaji": "yu", "sound": "ю"},
    "ヨ": {"romaji": "yo", "sound": "ё"},
    
    # R-ряд
    "ラ": {"romaji": "ra", "sound": "ра"},
    "リ": {"romaji": "ri", "sound": "ри"},
    "ル": {"romaji": "ru", "sound": "ру"},
    "レ": {"romaji": "re", "sound": "рэ"},
    "ロ": {"romaji": "ro", "sound": "ро"},
    
    # W-ряд и N
    "ワ": {"romaji": "wa", "sound": "ва"},
    "ヲ": {"romaji": "wo", "sound": "во"},
    "ン": {"romaji": "n", "sound": "н"}
}

# Комбинированные наборы хираганы
HIRAGANA_FULL_DATA = {**HIRAGANA_DATA, **HIRAGANA_DAKUTEN_DATA}

# Типы викторин
QUIZ_TYPES = {
    # Кандзи викторины
    "kanji": {
        "name": "🈳 Кандзи → Значение",
        "data": KANJI_DATA,
        "folder": "data/kanji",
        "question": "Что означает этот иероглиф?",
        "answer_type": "meaning",
        "show_symbol": True
    },
    
    # Хирагана викторины
    "hiragana_to_romaji": {
        "name": "🈶 Хирагана → Romaji",
        "data": HIRAGANA_DATA,
        "folder": "data/hiragana",
        "question": "Как читается этот символ хираганы?",
        "answer_type": "romaji",
        "show_symbol": True
    },
    "romaji_to_hiragana": {
        "name": "🔤 Romaji → Хирагана",
        "data": HIRAGANA_DATA,
        "folder": "data/hiragana",
        "question": "Какой символ хираганы соответствует этому чтению?",
        "answer_type": "symbol",
        "show_symbol": False
    },
    
    # Хирагана с тэнтэн и мару
    "hiragana_dakuten_to_romaji": {
        "name": "🈶゛゜ Тэнтэн/Мару → Romaji",
        "data": HIRAGANA_DAKUTEN_DATA,
        "folder": "data/hiragana_dakuten",
        "question": "Как читается этот символ хираганы с тэнтэн/мару?",
        "answer_type": "romaji",
        "show_symbol": True
    },
    "romaji_to_hiragana_dakuten": {
        "name": "🔤 Romaji → Тэнтэн/Мару",
        "data": HIRAGANA_DAKUTEN_DATA,
        "folder": "data/hiragana_dakuten",
        "question": "Какой символ хираганы с тэнтэн/мару соответствует этому чтению?",
        "answer_type": "symbol",
        "show_symbol": False
    },
    
    # Полная хирагана (базовая + тэнтэн + мару)
    "hiragana_full_to_romaji": {
        "name": "🈶 Полная Хирагана → Romaji",
        "data": HIRAGANA_FULL_DATA,
        "folder": "data/hiragana_full",
        "question": "Как читается этот символ хираганы?",
        "answer_type": "romaji",
        "show_symbol": True
    },
    "romaji_to_hiragana_full": {
        "name": "🔤 Romaji → Полная Хирагана",
        "data": HIRAGANA_FULL_DATA,
        "folder": "data/hiragana_full",
        "question": "Какой символ хираганы соответствует этому чтению?",
        "answer_type": "symbol",
        "show_symbol": False
    },
    
    # Катакана викторины
    "katakana_to_romaji": {
        "name": "🈯 Катакана → Romaji",
        "data": KATAKANA_DATA,
        "folder": "data/katakana",
        "question": "Как читается этот символ катаканы?",
        "answer_type": "romaji",
        "show_symbol": True
    },
    "romaji_to_katakana": {
        "name": "🔤 Romaji → Катакана",
        "data": KATAKANA_DATA,
        "folder": "data/katakana",
        "question": "Какой символ катаканы соответствует этому чтению?",
        "answer_type": "symbol",
        "show_symbol": False
    }
}
