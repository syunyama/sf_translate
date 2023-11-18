from concurrent.futures import ThreadPoolExecutor, wait
import xml.etree.ElementTree as ET
from sf_translate.services.xml import LabelXML
from sf_translate.data import TranslateChunk
from sf_translate.services.translator import ITranslator
from sf_translate.services.editor import IEditor
from sf_translate.constants import MAX_WORKERS

class LabelXMLEditor(IEditor):
    def __init__(
        self,
        translator: ITranslator,
        input_path,
        output_path,
        target_lang,
        source_lang=None,
        max_workers=MAX_WORKERS,
    ):
        self._translator = translator
        self._xml = LabelXML(input_path, output_path, target_lang, source_lang)
        self._max_workers = max_workers

    def _edit(self, chunk: TranslateChunk):
        label = chunk.chunk.find("label")
        translated_text = self._translator.translate(
            label.text, chunk.target_lang, chunk.source_lang
        )
        label.text = translated_text

    def translate(self):
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            futures = [
                executor.submit(self._edit, chunk) for chunk in self._xml.get_chunks()
            ]
        wait(futures)
        self._xml.write()
