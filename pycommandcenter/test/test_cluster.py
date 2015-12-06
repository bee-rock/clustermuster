from pycommandcenter.cluster import Cluster, ClusterNode
import base
from Queue import Queue


class Test(base.CQSTest):
    
    def setUp(self):
        self.cluster = Cluster(Queue())
        self.address = "some_address"
        self.port = 22
    
    def test_add_node(self):
        self.cluster.add_node(self.address, self.port)
        self.assertEquals(1, self.cluster.number_of_nodes_available())
        
    def test_number_of_nodes_available(self):
        self.assertEquals(0, self.cluster.number_of_nodes_available())
        
    def test_no_command_available(self):
        self.assertEquals(None, self.cluster.get_command())

    def test_get_node(self):
        node = ClusterNode("some_address", 22)
        self.assertTrue(node.is_available())
        self.cluster.add_node(self.address, self.port)
        node = self.cluster.get_available_node()
        self.assertTrue(node is not None)
        self.assertEquals(node.address, self.address)
        self.assertEquals(node.port, self.port)

