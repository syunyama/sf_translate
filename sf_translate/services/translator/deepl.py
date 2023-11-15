import requests
from sf_translate.services.translator import ITranslator
from sf_translate.data import TranslateChunk
from sf_translate.constant import SALESFORCE_SUPPORTED_LANGUAGES


class DeepLTranslator(ITranslator):
    def __init__(self, auth_key):
        self._auth_key = auth_key

    def _convert_lang(self, lang):
        # https://www.deepl.com/ja/docs-api/translate-text/translate-text
        if lang not in SALESFORCE_SUPPORTED_LANGUAGES:
            raise ValueError(f'Language "{lang}" is not supported')
        return lang[:2].upper()

    def _call(self, source, target_lang, source_lang):
        target_lang = self._convert_lang(target_lang)
        source_lang = self._convert_lang(source_lang)
        print(f'Calling DeepL API with "{source}" to translate to "{target_lang}"')
        params = {
            "auth_key": self._auth_key,
            "text": source,
            "source_lang": source_lang,
            "target_lang": target_lang,
        }
        request = requests.post("https://api-free.deepl.com/v2/translate", data=params)
        json = request.json()
        return json["translations"][0]["text"]

    def translate(self, source, target_lang, source_lang):
        try:
            return self._call(source, target_lang, source_lang)
        except Exception as e:
            print(f'Error: {e} for "{source}"')
