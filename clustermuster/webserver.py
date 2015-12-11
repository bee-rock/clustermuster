import SocketServer
import json
import logging


logger = logging.getLogger(__name__)


class TCPHandler(SocketServer.ThreadingMixIn, SocketServer.BaseRequestHandler):

    def __init__(self, callback, *args, **keys):
        self.callback = callback
        SocketServer.BaseRequestHandler.__init__(self, *args, **keys)

    def handle(self):
        logger.debug("Got command")
        command = self.request.recv(1024).strip()
        self.callback(command)


class WebServer(SocketServer.TCPServer):
    def __init__(self, host, port, commands, TCPHandler):
        SocketServer.ThreadingTCPServer.allow_reuse_address = True
        SocketServer.TCPServer.__init__(self, (host, port), TCPHandler, bind_and_activate=False)
        self.socket.setsockopt(SocketServer.socket.SOL_SOCKET, SocketServer.socket.SO_REUSEADDR, 1)
        self.server_bind()
        self.server_activate()
        self.commands = commands

    def command_handler(self, command):
        try:
            self.commands.put(json.loads(command))
            logger.debug("Put command into queue")
        except ValueError:
            logger.debug("Could not put command into queue")
            pass
