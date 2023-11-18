from concurrent.futures import ThreadPoolExecutor, wait
import xml.etree.ElementTree as ET
from sf_translate.services.property import BasicProperty
from sf_translate.data import TranslateChunk
from sf_translate.services.translator import ITranslator
from sf_translate.services.editor import IEditor
from sf_translate.constants import MAX_WORKERS

class PropertyEditor(IEditor):
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
        self._property = BasicProperty(input_path, output_path, target_lang, source_lang)
        self._max_workers = max_workers

    def _edit(self, chunk: TranslateChunk):
        
        for k, v in chunk.chunk.items():
            chunk.chunk[k] = self._translator.translate(
                v, chunk.target_lang, chunk.source_lang
            )

    def translate(self):
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            futures = [
                executor.submit(self._edit, chunk) for chunk in self._property.get_chunks()
            ]
        wait(futures)
        self._property.write()
