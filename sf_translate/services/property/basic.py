import os
import abc
import configparser
import json
import xml.etree.ElementTree as ET
from sf_translate.services.property import IProperty
from sf_translate.data import TranslateChunk


class BasicProperty(IProperty):
    _SEPARATOR = "="
    _HO_HEADER_KEY = "NO_HEADER"

    def __init__(self, input_path, output_path, target_lang, source_lang=None):
        self._input_path = input_path
        self._output_path = output_path
        self._target_lang = target_lang
        self._source_lang = source_lang
        self._dictionary = {}

    def get_chunks(self):
        try:
            config = configparser.ConfigParser()
            config.read(self._input_path)
            sections = config.sections()
            for section in sections:
                for k, v in config[section].items():
                    if section not in self._dictionary:
                        self._dictionary[section] = []
                    value = {k: v}
                    self._dictionary[section].append(value)
                    yield TranslateChunk(
                        value,
                        self._target_lang,
                        self._source_lang,
                    )
        except configparser.MissingSectionHeaderError as e:
            with open(self._input_path) as f:
                for line in f:
                    if self._SEPARATOR in line:
                        k, v = line.split(self._SEPARATOR, 1)
                        if self._HO_HEADER_KEY not in self._dictionary:
                            self._dictionary[self._HO_HEADER_KEY] = []
                        value = {k: v}
                        self._dictionary[self._HO_HEADER_KEY].append(value)
                        yield TranslateChunk(
                            value,
                            self._target_lang,
                            self._source_lang,
                        )

    def write(self):
        dir_path = os.path.dirname(self._output_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(self._output_path, "w") as f:
            for section, v in self._dictionary.items():
                if section != self._HO_HEADER_KEY:
                    f.write(f"[{section}]\n")
                for item in v:
                    for key, value in item.items():
                        f.write(key + self._SEPARATOR + value + "\n")
