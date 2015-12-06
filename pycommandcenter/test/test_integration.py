from pycommandcenter.servercontroller import ServerController
from pycommandcenter.cluster import ClusterNode
from utils import TestClient
import time
import base
import mock


def SendCommand(command):
    client = TestClient("localhost", 9999)
    client.send_command(command)
    time.sleep(0.5) # Give server some time to receive it
    client.close()


class Test(base.CQSTest):
    def setUp(self):
        self.controller = ServerController()
        self.controller.start_server()
        self.command_to_send = "sweet_command_bro"
        self.node_address = "some_address"
        self.node_port = 22
        
    def tearDown(self):
        self.controller.stop_server()
    
    def test_client_command(self):
        SendCommand(self.command_to_send)
        time.sleep(0.5)
        retreived_command = self.controller.cluster.get_command()
        self.assertEquals(self.command_to_send, retreived_command)

    @mock.patch.object(ClusterNode, 'send_command')
    def test_handoff_command_to_node(self, mock_send_command):
        self.controller.cluster.add_node(self.node_address, self.node_port)
        SendCommand(self.command_to_send)
        self.controller.cluster.execute_node()
        mock_send_command.assert_called_with(self.command_to_send)
        node = self.controller.cluster.get_available_node()
        node.send_command.assert_called_with(self.command_to_send)
        
        
        