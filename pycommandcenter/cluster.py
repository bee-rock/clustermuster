from Queue import Empty
import subprocess


class ClusterNode(object):
    
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.available = True
        
    def available(self):
        return self.available
    
    def send_command(self, command):
        process = subprocess.Popen("ssh " + self.address + " " + command, shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # Install public key to avoid password
        output,stderr = process.communicate()
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
        except Empty as queue_is_empty:
            pass
    
    def add_existing_node(self, cluster_node):
        self.nodes.append(cluster_node)
        
    def add_new_node(self, address, port):
        self.nodes.append(ClusterNode(address, port))
        
    def number_of_nodes_available(self):
        return len(self.nodes)
        
    def get_available_node(self):
        for node in self.nodes:
            if node.available:
                return node
