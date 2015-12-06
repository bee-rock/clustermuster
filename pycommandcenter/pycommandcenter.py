import sys
import argparse
import yaml
from servercontroller import ServerController


def main():
    parser = argparse.ArgumentParser()
    parser.parse_args()
    parser.add_argument('filename')
    args = parser.parse_args()
    configuration = yaml.load(open(args.filename).read())
    controller = ServerController()
    for node in configuration['nodes']:
        controller.cluster.add_node(node['address'], node['port'])
    try:
        controller.start_server()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print "%s" % e
        sys.exit(-1)
