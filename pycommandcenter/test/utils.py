import socket


class TestClient(object):
    def __init__(self, host, port):
        HOST, PORT = host, port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
    
    def send_command(self, command):
        self.sock.send(command)

    def close(self):
        self.sock.close()

        
def null_callback():
    pass
