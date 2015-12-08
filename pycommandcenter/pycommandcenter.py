import sys
import argparse
import yaml
from servercontroller import ServerController
import os


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="filename", required=True,
                    help="nodes.yaml", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()
    configuration = yaml.load(args.filename.read())
    controller = ServerController()
    for _, value in configuration['nodes'].iteritems():
        controller.cluster.add_node(value['address'], value['port'])

    try:
        controller.start_server()
        while True:
            pass
    except KeyboardInterrupt:
        print "Keyboard interrrupted."
        controller.stop_server()
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print "%s" % e
        sys.exit(-1)
