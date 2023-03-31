from collections import namedtuple
from .option import Option

OptionResult = namedtuple('OptionResult', 'selected_option callback_result')


class FunctionalOption(Option):

    def __init__(self, id="default", description=None, callback=None, callback_params=None):
        Option.__init__(self, id, description)
        self.__callback = callback
        self.__callback_params = callback_params

    def select(self):
        if self.__callback_params:
            callback_result = self.__callback(*self.__callback_params)
        else:
            callback_result = self.__callback()
        return OptionResult(self.id, callback_result)

    def set_callback(self, callback):
        self.__callback = callback

    def add_callback_param(self, param):
        self.__callback_params.append(param)
