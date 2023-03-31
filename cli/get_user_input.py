from functools import partial
from menu_handler import Menu
from data_to_option import clients_to_options, commands_to_options


def get_client_from_user(io, shared_data):
    fetch_client_options = partial(clients_to_options, shared_data)
    clients_menu = Menu(io, fetch_client_options, 'Please select a client')
    selected_client = clients_menu.start()
    return selected_client


def get_command_from_user(io):
    commands_menu = Menu(io, commands_to_options, 'Please select a command')
    selected_command = commands_menu.start()
    return selected_command


def validate_command_args(command, args):
    """Returns True if args are valid, return str consists of the error message if invalid."""
    if not command.should_force_args():
        return True
    if args.strip() == "":
        return "Args cannot be empty"
    return True


def get_command_args_from_user(io, command):
    io.print('Please enter command args: (Insert \'abort\' for cancel operation)')
    args = ""
    validation_result = ""
    while isinstance(validation_result, str):
        if validation_result:
            io.print(validation_result)
        args = io.get_input()
        if args == "abort":
            return args
        validation_result = validate_command_args(command, args)
    return args.split(' ')  # TODO don't split by spaces when inside ""