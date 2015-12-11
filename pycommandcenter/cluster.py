from Queue import Empty
from subprocess import Popen, PIPE, STDOUT
import json
from schema import validate_json
import time
from jsonschema import ValidationError
import logging

logger = logging.getLogger(__name__)


class ClusterNode(object):

    def __init__(self, username, address, port):
        self.address = address
        self.port = port
        self.available = True
        self.username = username
        self.error_output_from_last_command = None
        self.result_from_last_command = None

    def is_available(self):
        return self.available

    def send_command(self, command):
        self.available = False
        logger.debug("Opening process on local to start connection to node")
        process = Popen(self.construct_command(command), shell=True,
                        stdout=PIPE, stderr=STDOUT)  # Install public key to avoid password
        self.result_from_last_command, self.error_output_from_last_command = process.communicate()
        logger.debug(self.result_from_last_command)
        if self.error_output_from_last_command:
            logger.debug(self.error_output_from_last_command)
        self.available = True

    def construct_command(self, command):
        return "ssh %s@%s '%s'" % (self.username, self.address, command)


class Cluster():
    def __init__(self, commands):
        self.nodes = []
        self.commands = commands
        self.polling = True

    def get_json(self):
        try:
            json = self.commands.get_nowait()
            validate_json(json)
            return json
        except Empty:
            return None
        except ValidationError:
            logger.debug(json)
            return json

    def add_node(self, username, ip_address, port):
        node = ClusterNode(username, ip_address, port)
        self.nodes.append(node)

    def number_of_nodes_available(self):
        return len(self.nodes)

    def get_available_node(self):
        if self.number_of_nodes_available() > 0:
            for node in self.nodes:
                if node.is_available():
                    return node

    def send_command_to_node(self, command):
            node = self.get_available_node()
            if node is None:
                logger.debug("No nodes available")
                return False
            node.available = False
            node.send_command(command)

    def poll_for_commands(self, poll_time=1):
        while True and self.polling is True:
            try:
                json_received = self.get_json()
            except ValidationError:
                logger.debug("Didn't pass validation")
                json_received = None
            if json_received is not None:
                logger.debug("Received command")
                command = json_received['command']
                if json_received['name'] == 'any':
                    logger.debug("Handing off to Node")
                    command_passed_to_node = self.send_command_to_node(command)
                    if command_passed_to_node is False:
                        self.commands.put(json_received)
            time.sleep(poll_time)

  