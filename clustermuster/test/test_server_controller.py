from clustermuster.servercontroller import ServerController
import base
import time


class Test(base.CQSTest):

    def setUp(self):
        server_port = 9999
        self.controller = ServerController(server_port)

    def assert_thread(self, thread):
        time.sleep(0.1)
        self.assertTrue(thread is not None)
        self.assertTrue(thread.isAlive())

    def test_start_and_stop_webserver(self):
        self.controller.start_server()
        self.assert_thread(self.controller.server_thread)
        self.controller.stop_server()
        self.assertFalse(self.controller.server_thread.isAlive())

    def test_start_poll_for_commands(self):
        self.controller.start_server()
        self.assert_thread(self.controller.cluster_thread)
        self.controller.stop_server()
        self.assertFalse(self.controller.cluster_thread.isAlive())
