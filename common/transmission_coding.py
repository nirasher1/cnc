import json
from .command_execution import CommandExecution
from .command_execution_status import CommandExecutionStatus
import base64


def encode_command(command_obj):
    return json.dumps(command_obj.to_dict()).encode()


def decode_command(command_bytecode):
    return CommandExecution.dict_to_command(json.loads(command_bytecode.decode()))


def encode_command_execution_status(obj):
    command_execution_status_dict = obj.to_dict()
    command_execution_status_dict['status'] = command_execution_status_dict['status'].value
    return base64.b64encode(json.dumps(command_execution_status_dict).encode())


def decode_command_execution_status(bytecode):
    command_execution_status_dict = json.loads(base64.b64decode(bytecode))
    return CommandExecutionStatus.dict_to_command(command_execution_status_dict)
