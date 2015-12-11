from clustermuster.test.utils import TestClient
from socket import error


def main():
    command = '{"name": "any", "command":"ls"}'
    client = TestClient("localhost", 9999)
    try:
        client.send_command(command)
    except error as e:
        print e
    finally:
        client.close()


if __name__ == "__main__":
    main()
