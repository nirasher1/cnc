from threading import Thread
from functools import partial
import logging
import sys
from pathlib import Path
from config import config
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from server import start_server, CommandsExecutionMonitor, parse_command_result
from cli_menu import start_cli

logger = logging.getLogger(__name__)


def main():
    shared_data = {
        'clients': {},
    }

    # Initialize manager of commands
    command_execution_monitor = CommandsExecutionMonitor()

    # Socket callback for parsing new data
    parse_command = partial(parse_command_result, command_execution_monitor)

    # Define socket thread
    socket_thread = Thread(target=start_server, args=[shared_data, parse_command], daemon=True)
    # Define cli thread
    cli_thread = Thread(target=start_cli, args=[shared_data, command_execution_monitor])

    # Starting threads
    logger.info('Starting server socket')
    socket_thread.start()
    logger.info('Starting CLI')
    cli_thread.start()


if __name__ == '__main__':
    logging.basicConfig(filename=config["LOG"]["LOGFILE"].replace('TIMESTAMP', str(datetime.timestamp(datetime.now()))),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    main()
