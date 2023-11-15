from concurrent.futures import ThreadPoolExecutor, wait
import xml.etree.ElementTree as ET
from sf_translate.services.xml import LabelXML
from sf_translate.data import TranslateChunk
from sf_translate.services.translator import ITranslator
from sf_translate.services.editor import IEditor


class LabelEditor(IEditor):
    def __init__(
        self,
        translator: ITranslator,
        xml_input_path,
        xml_output_path,
        target_lang,
        source_lang=None,
    ):
        self._translator = translator
        self._xml = LabelXML(xml_input_path, xml_output_path, target_lang, source_lang)

    def _edit(self, chunk: TranslateChunk):
        label = chunk.chunk.find("label")
        translated_text = self._translator.translate(
            label.text, chunk.target_lang, chunk.source_lang
        )
        label.text = translated_text

    def translate(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(self._edit, chunk) for chunk in self._xml.get_chunks()
            ]
        wait(futures)
        self._xml.write()
