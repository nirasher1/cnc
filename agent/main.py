from threading import Thread
from collections import deque
from functools import partial
from commands_handler import CommandsHandler
import sys
from pathlib import Path
import logging
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from config import config
from connection import start_agent
from commands_execution_utils import start_commands_executor
from common import encode_command_execution_status, CommandExecutionStatus

logger = logging.getLogger(__name__)


def update_command_status(messages_to_server, command, status, message=""):
    exec_id = command.get_exec_id()

    logger.info(f'Sending command with exec_id {exec_id} status "{status}" to server')
    execution_status = CommandExecutionStatus(exec_id, status, message)
    messages_to_server.append(encode_command_execution_status(execution_status))


def main():
    messages_to_server = deque()

    commands_handler = CommandsHandler(config['FUNCTIONAL']['PAYLOAD_FOLDER'])

    update_status = partial(update_command_status, messages_to_server)

    # Data producer
    socket_thread = Thread(target=start_agent, args=[commands_handler, messages_to_server])
    # Data consumer
    commands_executor_thread = Thread(target=start_commands_executor, args=[commands_handler, update_status],
                                      daemon=True)

    logger.info('Starting socker thread')
    socket_thread.start()
    logger.info('Starting command executor listener thread')
    commands_executor_thread.start()


if __name__ == '__main__':
    logging.basicConfig(filename=config["LOG"]["LOGFILE"].replace('TIMESTAMP', str(datetime.timestamp(datetime.now()))),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    main()
