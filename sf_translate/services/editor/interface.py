import abc


class IEditor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def translate(self):
        raise NotImplementedError()
