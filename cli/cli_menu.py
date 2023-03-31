import sys

from commands_execution_monitor_view import CommandsExecutionMonitorView
from menu_handler import Menu, FunctionalOption
from common import input_output
from server import send_to_client, close_client_sock
from print_status_utils import print_status
from get_user_input import get_client_from_user, get_command_from_user, get_command_args_from_user


def start_cli(shared_data, commands_execution_monitor):
    io = input_output.ConsoleIO()

    commands_monitor_view = CommandsExecutionMonitorView(io, commands_execution_monitor)

    options = [
        FunctionalOption('send', 'Send command', send_command, [io, shared_data, commands_execution_monitor]),
        FunctionalOption('kill', 'Kill client', kill_client, [io, shared_data]),
        FunctionalOption('status', 'show status of cliens\' commands', print_status, [io, commands_monitor_view]),
        FunctionalOption('exit', 'exit', exit_program)
    ]
    menu = Menu(io, options)
    while True:
        menu.start()


def send_command(io, shared_data, execution_manager):
    selected_client_option = get_client_from_user(io, shared_data)
    if selected_client_option.get_id() == 'abort':
        return
    selected_command_option = get_command_from_user(io)
    if selected_command_option.get_id() == 'abort':
        return
    command_obj = selected_command_option.get_payload()
    if command_obj.is_accept_args():
        selected_command_args = get_command_args_from_user(io, command_obj)
        if selected_command_args == "abort":
            return
        command_obj.set_payload_args(selected_command_args)
    if selected_client_option.get_id() == 'all':
        send_to_client(shared_data['clients'].values(), command_obj, execution_manager)
    else:
        send_to_client([selected_client_option.get_payload()[0]], command_obj, execution_manager)


def kill_client(io, shared_data):
    selected_client_option = get_client_from_user(io, shared_data)
    if selected_client_option.get_id() == 'abort':
        return
    sock, client_id = selected_client_option.get_payload()
    del shared_data['clients'][client_id]
    close_client_sock(sock, client_id)


def exit_program():
    sys.exit()
