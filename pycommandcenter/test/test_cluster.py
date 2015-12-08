from pycommandcenter.cluster import Cluster, ClusterNode
import base
from Queue import Queue


class Test(base.CQSTest):

    def setUp(self):
        self.cluster = Cluster(Queue())
        self.username = "cooluser"
        self.address = "some_address"
        self.port = 22

    def test_add_node(self):
        self.cluster.add_node(self.username, self.address, self.port)
        self.assertEquals(1, self.cluster.number_of_nodes_available())

    def test_number_of_nodes_available(self):
        self.assertEquals(0, self.cluster.number_of_nodes_available())

    def test_no_json_available(self):
        self.assertEquals(None, self.cluster.get_json())

    def test_get_node(self):
        node = ClusterNode(self.username, self.address, self.port)
        self.assertTrue(node.is_available())
        self.cluster.add_node(self.username, self.address, self.port)
        node = self.cluster.get_available_node()
        self.assertTrue(node is not None)
        self.assertEquals(node.address, self.address)
        self.assertEquals(node.username, self.username)
        self.assertEquals(node.port, self.port)

    def test_construct_command(self):
        node = ClusterNode(self.username, self.address, self.port)
        constructed_command = node.construct_command("ls -l")
        self.assertEquals("ssh cooluser@some_address 'ls -l'", constructed_command)
