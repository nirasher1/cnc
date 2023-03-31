from queue import Queue
from os import path, remove
from pathlib import Path


class CommandsHandler:
    """
    Holds commands queue and manage popping of command from the queue.
    """

    def __init__(self, payload_folder):
        self.__to_handle = Queue()
        self.__payload_folder = path.dirname(path.realpath(__file__)) + payload_folder
        Path(self.__payload_folder).mkdir(parents=True, exist_ok=True)

    def add_command(self, command):
        self.__write_payload_file(command)
        self.__to_handle.put(command)

    def get_command_to_handle(self):
        command = self.__to_handle.get()

        payload_file_path = self.__get_payload_file_path(command)
        with open(payload_file_path, "r") as payload_file:
            command_payload = payload_file.read()
            payload_file.close()

        return [command, command_payload]

    def cleanup_command(self, command):
        payload_file_path = self.__get_payload_file_path(command)
        remove(payload_file_path)

    def __write_payload_file(self, command):
        payload_file_path = self.__get_payload_file_path(command)

        with open(payload_file_path, "w") as payload_file:
            payload_file.write(command.get_payload())
            payload_file.close()

    def __read_payload_file(self, command):
        payload_file_path = self.__get_payload_file_path(command)

        with open(payload_file_path, "r") as payload_file:
            payload_file.write(command.get_payload())
            payload_file.close()

    def __get_payload_file_path(self, command):
        return path.join(self.__payload_folder, str(command.get_exec_id()))
