from .io_base import IOBase
import os


class ConsoleIO(IOBase):
    def print(self, message):
        print(message)

    def clear(self):
        os.system('cls')

    def get_input(self, message=''):
        return input(message)
