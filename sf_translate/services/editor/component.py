from concurrent.futures import ThreadPoolExecutor, wait
from sf_translate.services.xml import ComponentXML
from sf_translate.data import TranslateChunk
from sf_translate.services.translator import ITranslator
from sf_translate.services.editor import IEditor


class ComponentEditor(IEditor):
    def __init__(self, translator: ITranslator, xml_input_path, xml_output_path):
        self._translator = translator
        self._xml = ComponentXML(xml_input_path, xml_output_path)

    def _edit(self, chunk: TranslateChunk):
        target = chunk.chunk.find(".//{urn:oasis:names:tc:xliff:document:2.0}target")
        source = chunk.chunk.find(".//{urn:oasis:names:tc:xliff:document:2.0}source")
        translated_text = self._translator.translate(
            source.text, chunk.target_lang, chunk.source_lang
        )
        target.text = translated_text

    def translate(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(self._edit, chunk) for chunk in self._xml.get_chunks()
            ]
        wait(futures)
        self._xml.write()
