import socket
import selectors
import logging

from .config import config

logger = logging.getLogger(__name__)

selector = selectors.DefaultSelector()


def start_server(shared_data, handle_message):
    """Starting a socket which allows get messages from clients, and send messaged to clients."""

    connection_config = config['CONNECTION']
    port = int(connection_config['PORT'])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((connection_config['HOST'], port))
    sock.listen()
    logger.info(f'Server starts listening on port {port}')
    sock.setblocking(False)
    selector.register(sock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = selector.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_new_connection(key.fileobj, shared_data)
                else:
                    handle_agent_message(key, mask, shared_data, handle_message)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        selector.close()


def accept_new_connection(sock, shared_data):
    conn, addr = sock.accept()
    shared_data["clients"][addr] = conn
    conn.setblocking(False)
    data = {"addr": addr, "outb": ""}
    selector.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)
    logger.info(f'Accepted new client {str(addr)}')


def handle_agent_message(key, mask, shared_data, handle_message):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        try:
            logger.info(f'Got message from client {str(data["addr"])}')
            recv_data = sock.recv(1024).decode()
            handle_message(recv_data)
        except ConnectionResetError:
            logger.info(f'Client {str(data["addr"])} has disconnected')
            del shared_data["clients"][data['addr']]
            selector.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data["outb"]:
            logger.info(f'Writing message to {str(data["addr"])}')
            sent = sock.send(data["outb"].encode())
            data["outb"] = data["outb"][sent:]


def close_client_sock(sock, client_id):
    selector.unregister(sock)
    sock.close()
    logger.info(f'Closing connection with client {client_id}')

