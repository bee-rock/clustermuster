from Queue import Empty
import subprocess


class ClusterNode(object):

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.available = True

    def is_available(self):
        return self.available

    def check_return_code(self, code):
        pass

    def check_error(self, error):
        pass

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

    def get_command(self):
        try:
            return self.commands.get_nowait()
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

    def execute_node(self):
        command = self.get_command()
        node = self.get_available_node()
        node.send_command(command)
