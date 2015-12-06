from Queue import Empty
import subprocess
import json
from schema import validate_json


class ClusterNode(object):

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.available = True
        self.name = None

    def is_available(self):
        return self.available

    def send_command(self, command):
        process = subprocess.Popen("ssh " + self.address + " " + command, shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # Install public key to avoid password
        output, stderr = process.communicate()
        self.check_return_code(output)
        self.check_error(stderr)
        status = process.poll()
        return status


class Cluster():
    def __init__(self, commands):
        self.nodes = []
        self.commands = commands
        self.wait_for_commands = True

    def get_json(self):
        try:
            return self.commands.get_nowait()
            validate_json(json)
        except Empty:
            return None

    def add_node(self, ip_address, port):
        node = ClusterNode(ip_address, port)
        self.nodes.append(node)

    def number_of_nodes_available(self):
        return len(self.nodes)

    def get_available_node(self):
        for node in self.nodes:
            if node.is_available():
                return node

    def get_node_by_name(self, name):
        pass

    def execute_node(self):
        json_received = self.get_json()

        if json_received['name'] == 'any':
            node = self.get_available_node()
            if node is None:
                self.commands.put(json_received)
                return None
            node.send_command(json_received['command'])
