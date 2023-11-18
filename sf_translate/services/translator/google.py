import requests
from sf_translate.services.translator import ITranslator
from sf_translate.data import TranslateChunk
from sf_translate.constants import SALESFORCE_SUPPORTED_LANGUAGES


class GoogleTranslator(ITranslator):
    def __init__(self, auth_key):
        self._auth_key = auth_key

    def _convert_lang(self, lang):
        # https://cloud.google.com/translate/docs/languages?hl=ja
        if lang is None:
            return None
        if lang not in SALESFORCE_SUPPORTED_LANGUAGES:
            raise ValueError(f'Language "{lang}" is not supported')
        return lang[:2]

    def _call(self, source, target_lang, source_lang=None):
        target_lang = self._convert_lang(target_lang)
        source_lang = self._convert_lang(source_lang)
        print(f'Calling Google API with "{source}" to translate to "{target_lang}"')
        params = {
            "key": self._auth_key,
            "q": source,
            "target": target_lang,
        }
        if source_lang:
            params["source"] = source_lang
        request = requests.post("https://translation.googleapis.com/language/translate/v2", params=params)
        json = request.json()
        return json["data"]["translations"][0]["translatedText"]

    def translate(self, source, target_lang, source_lang=None):
        try:
            return self._call(source, target_lang, source_lang)
        except Exception as e:
            print(f'Error: {e} for "{source}"')
