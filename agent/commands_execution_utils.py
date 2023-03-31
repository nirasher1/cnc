from threading import Thread
import subprocess
import logging

from common import ExecutionStatus

logger = logging.getLogger(__name__)


def generate_command_string(payload, payload_args):
    """ Generate actual terminal command """
    args_string = ' '.join(payload_args)
    if args_string:
        return f'{payload} {args_string}'
    return payload


def run_command(command, command_payload, update_status):
    """Get command and execute it as a process"""
    update_status(command, ExecutionStatus.RUNNING)

    parsed_command = generate_command_string(command_payload, command.get_payload_args())
    try:
        logger.info(f'Start running command {command.get_exec_id()} by "{parsed_command}"')
        result = subprocess.check_output(parsed_command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as error:
        logger.error(f'Failed running command {command.get_exec_id()}. reason: {str(error)}')
        update_status(command, ExecutionStatus.ERROR, str(error))
        return

    logger.info(f'Command {command.get_exec_id()} running has completed successfully')
    update_status(command, ExecutionStatus.FINISHED, str(result))


def start_commands_executor(commands_handler, update_status):
    """Listening to commands queue and start execution process."""
    while True:
        # Command payload here is the actual command name! we dont really need this, but the insructions ask for reading it from file, so this is the file read result
        command_obj, command_payload = commands_handler.get_command_to_handle()
        command_thread = Thread(target=run_command, args=[command_obj, command_payload, update_status])
        update_status(command_obj, ExecutionStatus.INITIALIZED)
        command_thread.start()
