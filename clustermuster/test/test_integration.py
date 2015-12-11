from clustermuster.servercontroller import ServerController
from clustermuster.cluster import ClusterNode
from utils import SendCommandFromClient
import base
import mock
import json
import time


class Test(base.CQSTest):
    def setUp(self):
        server_port = 9999
        self.controller = ServerController(server_port)
        self.controller.start_server()
        self.username = "cooluser"
        self.node_address = "some_address"
        self.node_port = 22

    def tearDown(self):
        self.controller.stop_server()

    def test_client_sent_invalid_json(self):
        invalid_json = "bad command bro"
        SendCommandFromClient(invalid_json)
        retreived_command = self.controller.cluster.get_json()
        self.assertTrue(retreived_command is None)

    @mock.patch.object(ClusterNode, 'send_command')
    def test_json_fits_schema_request_with_node_available(self, mock_send_command):
        self.controller.cluster.add_node(self.username, self.node_address, self.node_port)
        valid_json = '{"name": "any", "command":"Rossum"}'
        SendCommandFromClient(valid_json)
        time.sleep(2)
        self.assertEquals(None, self.controller.cluster.get_json())


    @mock.patch.object(ClusterNode, 'send_command')
    def test_json_fits_schema_request_without_node_available(self, mock_send_command):
        #self.controller.cluster.add_node(self.username, self.node_address, self.node_port)
        valid_json = '{"name": "any", "command":"Rossum"}'
        SendCommandFromClient(valid_json)
        time.sleep(2)
        self.assertEquals(json.loads(valid_json), self.controller.cluster.get_json())

    @mock.patch.object(ClusterNode, 'send_command')
    def test_handoff_command_to_node(self, mock_send_command):
        valid_json = '{"name": "any", "command":"Rossum"}'
        parsed_json = json.loads(valid_json)
        command_to_send = parsed_json['command']
        self.controller.cluster.add_node(self.username, self.node_address, self.node_port)
        self.assertEquals(1, self.controller.cluster.number_of_nodes_available())
        self.controller.cluster.send_command_to_node(command_to_send)
        mock_send_command.assert_called_with(command_to_send)

