from pycommandcenter.servercontroller import ServerController
import base


class Test(base.CQSTest):

    def assert_thread(self, thread):
        self.assertTrue(thread is not None)
        self.assertTrue(thread.isAlive())

    def test_start_and_stop_webserver(self):
        controller = ServerController()
        controller.start_server()
        self.assert_thread(controller.server_thread)
        controller.stop_server()
        self.assertFalse(controller.server_thread.isAlive())

    def test_start_poll_for_commands(self):
        controller = ServerController()
        controller.start_server()
        self.assert_thread(controller.cluster_thread)
        controller.stop_server()
        self.assertFalse(controller.cluster_thread.isAlive())
