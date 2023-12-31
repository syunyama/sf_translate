import os
import abc
import xml.etree.ElementTree as ET
from sf_translate.services.xml import IXML
from sf_translate.data import TranslateChunk


class DataXML(IXML):
    def __init__(self, input_path, output_path, target_lang, source_lang):
        self._input_path = input_path
        self._output_path = output_path
        self._tree = ET.parse(self._input_path)
        self._target_lang = target_lang
        self._source_lang = source_lang
        self._root = self._tree.getroot()
        file = self._root.find("file")
        file.set("source-language", self._source_lang)
        file.set("target-language", self._target_lang)

    def get_chunks(self):
        for chunk in self._root.findall(".//trans-unit"):
            yield TranslateChunk(chunk, self._target_lang, self._source_lang)

    def write(self):
        dir_path = os.path.dirname(self._output_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self._tree.write(self._output_path, encoding="utf-8", xml_declaration=True)
