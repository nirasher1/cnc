from abc import ABC, abstractmethod

class IOBase(ABC):
    @abstractmethod
    def print(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def get_input(self):
        pass

