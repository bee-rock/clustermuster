from pycommandcenter.test.utils import SendCommandFromClient
from socket import error


def main():
    command = '{"name": "any", "command":"Rossum"}'
    try:
        SendCommandFromClient(command)
    except error as e:
        print e

if __name__ == "__main__":
    main()
