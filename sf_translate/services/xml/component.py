import abc
import xml.etree.ElementTree as ET
from sf_translate.services.xml import IXML
from sf_translate.data import TranslateChunk


class ComponentXML(IXML):
    def __init__(self, xml_input_path, xml_output_path):
        self._xml_input_path = xml_input_path
        self._xml_output_path = xml_output_path
        self._tree = ET.parse(self._xml_input_path)
        self._root = self._tree.getroot()
        self._target_lang = self._root.attrib["trgLang"].replace('-', '_')
        self._source_lang = self._root.attrib["srcLang"].replace('-', '_')

    def get_chunks(self):
        for chunk in self._root.findall(
            ".//{urn:oasis:names:tc:xliff:document:2.0}segment"
        ):
            yield TranslateChunk(chunk, self._target_lang, self._source_lang)

    def write(self):
        ET.register_namespace("", "urn:oasis:names:tc:xliff:document:2.0")
        ET.register_namespace("fs", "urn:oasis:names:tc:xliff:fs:2.0")
        self._tree.write(self._xml_output_path, encoding="utf-8", xml_declaration=True)
