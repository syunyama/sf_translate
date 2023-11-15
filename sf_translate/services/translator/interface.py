import abc
from sf_translate.data import TranslateChunk


class ITranslator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def translate(self, chunk: TranslateChunk):
        raise NotImplementedError()
