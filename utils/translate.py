from googletrans import Translator


def translate_korean_to_english(from_word):
    translator = Translator()
    translated = translator.translate(from_word, dest="en")
    to_word = translated.text
    return to_word
