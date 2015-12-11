import webserver
import threading
from cluster import Cluster
from Queue import Queue
import logging

logger = logging.getLogger(__name__)


class ServerController(object):

    def __init__(self, port=9999):
        self.commands = Queue()
        self.cluster = Cluster(self.commands)
        self.server = webserver.WebServer("localhost",
                                          port,
                                          self.commands,
                                          lambda *args,
                                          **keys: webserver.TCPHandler(self.server.command_handler, *args, **keys))
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.cluster_thread = threading.Thread(target=self.cluster.poll_for_commands)

    def stop_server(self):
        self.server.server_close()
        self.server.shutdown()
        self.cluster.polling = False
        if self.server_thread is not None and self.server_thread.isAlive():
            self.server_thread.join()

        if self.cluster_thread is not None and self.cluster_thread.isAlive():
            self.cluster_thread.join()

    def start_server(self):
        self.server_thread.start()
        self.cluster_thread.start()
