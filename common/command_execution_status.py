from .execution_status import ExecutionStatus


class CommandExecutionStatus:
    """Status of specific execution"""

    def __init__(self, exec_id, status, message):
        self.__exec_id = exec_id
        self.__status = status
        self.__message = message

    def get_status(self):
        return self.__status

    def get_message(self):
        return self.__message

    def get_exec_id(self):
        return self.__exec_id

    def to_dict(self):
        return {
            'exec_id': self.__exec_id,
            'status': self.__status,
            'message': self.__message
        }

    @staticmethod
    def dict_to_command(dict):
        return CommandExecutionStatus(dict['exec_id'], ExecutionStatus(dict['status']), dict['message'])
