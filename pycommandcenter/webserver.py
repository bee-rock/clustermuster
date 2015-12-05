import SocketServer


class TCPHandler(SocketServer.BaseRequestHandler):

    def __init__(self, callback, *args, **keys):
        self.callback = callback
        SocketServer.BaseRequestHandler.__init__(self, *args, **keys)

    def handle(self):
        command = self.request.recv(1024).strip()
        self.callback(command)


class WebServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self, host, port, commands, TCPHandler):
        SocketServer.ThreadingTCPServer.allow_reuse_address = True
        SocketServer.TCPServer.__init__(self, (host, port), TCPHandler, bind_and_activate=False)
        self.socket.setsockopt(SocketServer.socket.SOL_SOCKET, SocketServer.socket.SO_REUSEADDR, 1)
        self.server_bind()
        self.server_activate()
        self.commands = commands

    def command_handler(self, command):
        self.commands.put(command)
