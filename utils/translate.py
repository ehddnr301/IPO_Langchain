from translate import Translator


def translate_korean_to_english(from_word):
    translator = Translator(to_lang="en", from_lang="ko")
    translated = translator.translate(from_word)
    return translated
