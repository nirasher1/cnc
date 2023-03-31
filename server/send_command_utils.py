import yaml
import os

from common import CommandExecution, encode_command, decode_command_execution_status


def get_commands_config():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "commands.yml"), "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config


def send_to_client(clients, data, execution_manager):
    """Add data for the server's writing buffer"""

    for client in clients:
        if isinstance(data, CommandExecution):
            execution_manager.get_executions()[data.get_exec_id()] = data
            client.send(encode_command(data))
        else:
            client.send(data.encode())


def parse_command_result(command_execution_monitor, command_result):
    """Parse received command statuses"""

    command_execution_status = decode_command_execution_status(command_result)
    command_execution_monitor.update_execution_status(command_execution_status)
