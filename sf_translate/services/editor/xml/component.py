from concurrent.futures import ThreadPoolExecutor, wait
from sf_translate.services.xml import ComponentXML
from sf_translate.data import TranslateChunk
from sf_translate.services.translator import ITranslator
from sf_translate.services.editor import IEditor
from sf_translate.constants import MAX_WORKERS


class ComponentXMLEditor(IEditor):
    def __init__(
        self,
        translator: ITranslator,
        input_path,
        output_path,
        max_workers=MAX_WORKERS,
    ):
        self._translator = translator
        self._xml = ComponentXML(input_path, output_path)
        self._max_workers = max_workers

    def _edit(self, chunk: TranslateChunk):
        target = chunk.chunk.find(".//{urn:oasis:names:tc:xliff:document:2.0}target")
        source = chunk.chunk.find(".//{urn:oasis:names:tc:xliff:document:2.0}source")
        translated_text = self._translator.translate(
            source.text, chunk.target_lang, chunk.source_lang
        )
        target.text = translated_text

    def translate(self):
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            futures = [
                executor.submit(self._edit, chunk) for chunk in self._xml.get_chunks()
            ]
        wait(futures)
        self._xml.write()
