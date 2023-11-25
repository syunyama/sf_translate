import os
import abc
import xml.etree.ElementTree as ET
from sf_translate.services.xml import IXML
from sf_translate.data import TranslateChunk


class StandardValueXML(IXML):
    def __init__(self, input_path, output_path, target_lang, source_lang=None):
        self._input_path = input_path
        self._output_path = output_path
        self._tree = ET.parse(self._input_path)
        self._target_lang = target_lang
        self._source_lang = source_lang
        self._root = self._tree.getroot()
        self._new_root = ET.Element(
            "StandardValueSetTranslation",
            attrib={"xmlns": "http://soap.sforce.com/2006/04/metadata"},
        )

    def get_chunks(self):
        for chunk in self._root.findall(
            ".//{http://soap.sforce.com/2006/04/metadata}standardValue"
        ):
            el_custom_labels = ET.SubElement(self._new_root, "valueTranslation")
            label = chunk.find("{http://soap.sforce.com/2006/04/metadata}label").text
            el_name = ET.SubElement(el_custom_labels, "masterLabel")
            el_name.text = label
            el_label = ET.SubElement(el_custom_labels, "translation")
            el_label.text = label
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
