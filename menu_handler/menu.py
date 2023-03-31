from .option import Option

DEFAULT_INSTRUCTION_MESSAGE = "Please select an option:"


class Menu(Option):
    """Selection menu functionality"""

    def __init__(self, io, options, message=DEFAULT_INSTRUCTION_MESSAGE, id="default", description=None):
        Option.__init__(self, id, description)
        self.__io = io
        self.__message = message
        if callable(options):
            self.__parse_options(options())
        else:
            self.__parse_options(options)

    def __parse_options(self, options):
        self.__options = options
        self.__add_back_option_to_submenu()
        self.__unique_name_to_option = {}
        self.__options_to_dict()

    def __add_back_option_to_submenu(self):
        for option in self.__options:
            if isinstance(option, Menu):
                option.add_back_option_to_array(self)

    def __options_to_dict(self):
        for option in self.__options:
            self.__unique_name_to_option[option.get_id()] = option

    def select(self):
        self.start()

    def start(self):
        self.__io.clear()
        self.__io.print(self.__str__())
        selected_option_name = self.__get_option_from_user()
        return self.__unique_name_to_option[selected_option_name].select()

    def add_back_option_to_array(self, menu):
        self.__options.append(menu)
        self.__unique_name_to_option[menu.get_id()] = menu

    def __get_option_from_user(self):
        self.__io.print(self.__message)
        user_input = None
        while user_input is None or not user_input in self.__unique_name_to_option:
            user_input = self.__io.get_input()
        return user_input

    def __str__(self, as_option=False):
        if as_option:
            return super(Menu, self).__str__()

        message = ''
        for option in self.__options:
            option_str = option.__str__(True) if isinstance(option, Menu) else option.__str__()
            message += option_str + '\r\n'
        return message


def build_menu(options):
    menu_options = []
    for id, description in options:
        menu_options.append(Option(id, description))
    return menu_options
