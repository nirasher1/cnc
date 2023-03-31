import logging
from datetime import datetime

from .connection import close_client_sock, start_server
from .commands_execution_monitor import CommandsExecutionMonitor
from .send_command_utils import send_to_client, get_commands_config, parse_command_result
from .config import config

# logging.basicConfig(filename=config["LOG"]["LOGFILE"].replace('TIMESTAMP', str(datetime.timestamp(datetime.now()))),
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG)
