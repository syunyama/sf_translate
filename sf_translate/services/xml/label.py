import os
import abc
import xml.etree.ElementTree as ET
from sf_translate.services.xml import IXML
from sf_translate.data import TranslateChunk


class LabelXML(IXML):
    def __init__(self, input_path, output_path, target_lang, source_lang=None):
        self._input_path = input_path
        self._output_path = output_path
        self._tree = ET.parse(self._input_path)
        self._target_lang = target_lang
        self._source_lang = source_lang
        self._root = self._tree.getroot()
        self._new_root = ET.Element(
            "Translations", attrib={"xmlns": "http://soap.sforce.com/2006/04/metadata"}
        )

    def get_chunks(self):
        for chunk in self._root.findall(
            ".//{http://soap.sforce.com/2006/04/metadata}labels"
        ):
            el_custom_labels = ET.SubElement(self._new_root, "customLabels")
            el_name = ET.SubElement(el_custom_labels, "name")
            el_name.text = chunk.find(
                "{http://soap.sforce.com/2006/04/metadata}fullName"
            ).text
            el_label = ET.SubElement(el_custom_labels, "label")
            el_label.text = chunk.find(
                "{http://soap.sforce.com/2006/04/metadata}value"
            ).text

            el_language = chunk.find(
                "{http://soap.sforce.com/2006/04/metadata}language"
            )
            source_lang = (
                el_language.text if el_language is not None else self._source_lang
            )
            yield TranslateChunk(
                el_custom_labels,
                self._target_lang,
                source_lang=self._source_lang,
            )

    def write(self):
        dir_path = os.path.dirname(self._output_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        ET.ElementTree(self._new_root).write(
            self._output_path, encoding="utf-8", xml_declaration=True
        )
