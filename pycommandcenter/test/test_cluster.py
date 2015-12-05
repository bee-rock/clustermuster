from pycommandcenter.cluster import Cluster, ClusterNode
import base
from Queue import Queue


class Test(base.CQSTest):
    
    def setUp(self):
        self.cluster = Cluster(Queue())
        self.address = "some_address"
        self.port = 22
        self.node = ClusterNode("some_address", 22)
    
    def test_add_node(self):
        self.cluster.add_existing_node(self.node)
        self.assertEquals(1, self.cluster.number_of_nodes_available())
        
    def test_number_of_nodes_available(self):
        self.assertEquals(0, self.cluster.number_of_nodes_available())

    def test_get_node(self):
        self.cluster.add_existing_node(self.node)
        node = self.cluster.get_available_node()
        self.assertTrue(node is not None)
        self.assertEquals(node.address, self.node.address)
        self.assertEquals(node.port, self.node.port)

    