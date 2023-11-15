from concurrent.futures import ThreadPoolExecutor, wait
import xml.etree.ElementTree as ET
from sf_translate.services.xml import DataXML
from sf_translate.data import TranslateChunk
from sf_translate.services.translator import ITranslator
from sf_translate.services.editor import IEditor


class DataEditor(IEditor):
    def __init__(
        self,
        translator: ITranslator,
        xml_input_path,
        xml_output_path,
        target_lang,
        source_lang,
    ):
        self._translator = translator
        self._xml = DataXML(xml_input_path, xml_output_path, target_lang, source_lang)

    def _edit(self, chunk: TranslateChunk):
        source = chunk.chunk.find("source")
        translated_text = self._translator.translate(
            source.text, chunk.target_lang, chunk.source_lang
        )
        target = ET.SubElement(chunk.chunk, "target")
        target.text = translated_text

    def translate(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(self._edit, chunk) for chunk in self._xml.get_chunks()
            ]
        wait(futures)
        self._xml.write()
