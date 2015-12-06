from pycommandcenter.servercontroller import ServerController
from pycommandcenter.cluster import ClusterNode
from utils import TestClient
import time
import base
import mock
import json
from jsonschema.exceptions import ValidationError


def SendCommand(command):
    client = TestClient("localhost", 9999)
    client.send_command(command)
    time.sleep(1)  # Give server some time to receive it
    client.close()


class Test(base.CQSTest):
    def setUp(self):
        self.controller = ServerController()
        self.controller.start_server()
        self.node_address = "some_address"
        self.node_port = 22

    def tearDown(self):
        self.controller.stop_server()

    def test_client_sent_invalid_json(self):
        invalid_json = "bad command bro"
        SendCommand(invalid_json)
        retreived_command = self.controller.cluster.get_json()
        self.assertTrue(retreived_command is None)

    def test_json_fits_schema_request(self):
        valid_json = '{"name": "any", "command":"Rossum"}'
        SendCommand(valid_json)
        self.assertEquals(json.loads(valid_json), self.controller.cluster.get_json())

    def test_json_does_not_fit_scheme(self):
        json_with_bad_schema = '{"first_name": "Guido", "last_name":"Rossum"}'
        self.assertRaises(ValidationError, self.controller.cluster.validate_json, json_with_bad_schema)

    @mock.patch.object(ClusterNode, 'send_command')
    def test_handoff_command_to_node(self, mock_send_command):
        valid_json = '{"name": "any", "command":"Rossum"}'
        parsed_json = json.loads(valid_json)
        self.controller.cluster.add_node(self.node_address, self.node_port)
        SendCommand(valid_json)
        self.controller.cluster.execute_node()
        mock_send_command.assert_called_with(parsed_json['command'])
        node = self.controller.cluster.get_available_node()
        node.send_command.assert_called_with(parsed_json['command'])
