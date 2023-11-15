import abc

class IXML(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_chunks(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def write(self):
        raise NotImplementedError()
