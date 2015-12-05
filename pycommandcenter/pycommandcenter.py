import sys
import pycommandcenter.webserver
import threading

def main():
    try:
        server = pycommandcenter.webserver.WebServer("localhost", 9999, lambda *args, **keys: pycommandcenter.webserver.TCPHandler(server.command_handler, *args, **keys))
        threading.Thread(target=server.serve_forever).start()
    except KeyboardInterrupt:
            server.socket.close()
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print "%s" % e
        sys.exit(-1)
    