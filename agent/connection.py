import socket
import selectors
import logging

from config import config
from common import decode_command

logger = logging.getLogger(__name__)

selector = selectors.DefaultSelector()


def start_agent(commands_handler, messages_to_server):
    connection_config = config['CONNECTION']

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((connection_config['HOST'], int(connection_config['PORT'])))
        sock.setblocking(True)
        logger.info('Connected to server')
        selector.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=messages_to_server)
        try:
            while True:
                events = selector.select(timeout=None)
                for key, mask in events:
                    data = key.data
                    if mask & selectors.EVENT_READ:
                        recv_data = sock.recv(1024)  # Should be ready to read
                        if recv_data:
                            logger.info('Received new command')
                            commands_handler.add_command(decode_command(recv_data))
                        else:
                            logger.info('Kicked by server. Closing connection')
                            selector.unregister(sock)
                            sock.close()
                    if mask & selectors.EVENT_WRITE:
                        if len(messages_to_server):
                            sock.send(data.popleft())

        except KeyboardInterrupt:
            logger.info('Keyboard interrupt. Closing connection')
        except ConnectionResetError as error:
            logger.info('Server is offline')
        finally:
            sock.close()
            return
