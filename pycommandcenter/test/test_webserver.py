from pycommandcenter.socketcontroller import ServerController
import base


class Test(base.CQSTest):
    
    def test_server_startup_and_shutdown(self):
        controller = ServerController()
        controller.start_server()
        self.assertTrue(controller.server_running)
        controller.stop_server()
        self.assertFalse(controller.server_running)
