import webserver
import threading
from cluster import Cluster
from Queue import Queue


class ServerController(object):
    
    def __init__(self):
        self.commands = Queue()
        self.cluster = Cluster(self.commands)
        self.server = webserver.WebServer("localhost", 9999, self.commands, lambda *args, **keys: webserver.TCPHandler(self.server.command_handler, *args, **keys))
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_running = None
        
    def stop_server(self):
        self.server.server_close()
        self.server.shutdown()
        self.server_running = False
        if self.server_thread is not None and self.server_thread.isAlive():
            self.server_thread.join()

    def start_server(self):
        self.server_thread = self.server_thread.start()
        self.server_running = True
