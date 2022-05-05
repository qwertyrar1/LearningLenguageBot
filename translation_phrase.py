from googletrans import Translator

translator = Translator()


def translate(phrase, leng):
    translation = translator.translate(phrase, dest=leng)
    return translation.text


