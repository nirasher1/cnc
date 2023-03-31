class CommandExecution:
    """Represents command execution (command + its specific execution properties (args, exec_id, etc.)"""

    __execution_id = 0

    def __init__(self, id, type, payload, accept_args=None, force_args=None, exec_id=None):
        self.__id = id
        self.__type = type
        self.__payload = payload
        self.__payload_args = []
        self.__accept_args = accept_args
        self.__force_args = force_args
        if exec_id:
            self.__exec_id = exec_id
        else:
            CommandExecution.__execution_id += 1
            self.__exec_id = CommandExecution.__execution_id

    def get_id(self):
        return self.__id

    def get_type(self):
        return self.__type

    def get_payload(self):
        return self.__payload

    def get_payload_args(self):
        return self.__payload_args

    def get_exec_id(self):
        return self.__exec_id

    def is_accept_args(self):
        return self.__accept_args

    def should_force_args(self):
        return self.__force_args

    def get_payload_args(self):
        return self.__payload_args

    def set_payload_args(self, payload_args):
        self.__payload_args = payload_args

    def to_dict(self):
        return {
            'id': self.__id,
            'type': self.__type,
            'payload': self.__payload,
            'payload_args': self.__payload_args,
            'exec_id': self.__exec_id
        }

    @staticmethod
    def dict_to_command(dict):
        command = CommandExecution(dict['id'], dict['type'], dict['payload'], exec_id=dict['exec_id'])
        command.set_payload_args(dict['payload_args'])
        return command
