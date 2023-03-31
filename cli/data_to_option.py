import uuid

from menu_handler import Option
from common import CommandExecution
from server import get_commands_config


def clients_to_options(shared_data):
    clients_data = shared_data['clients']
    client_options = []
    for index, client in enumerate(clients_data.keys(), start=1):
        client_options.append(Option(str(index), str(client), [clients_data[client], client]))
    client_options.append(Option('all', 'select all clients'))
    client_options.append(Option('abort', 'abort action'))
    return client_options


def commands_to_options():
    commands_config = get_commands_config()
    command_options = []
    for command_id, command_data in commands_config.items():
        command = CommandExecution(uuid.uuid4().int, 'bla', command_data['command'], command_data['accept_args'],
                                   command_data['force_args'])
        command_options.append(Option(str(command_id), command_data['description'], command))
    command_options.append(Option('abort', 'abort action'))
    return command_options
