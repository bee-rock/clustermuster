import sys
import argparse
import yaml
from servercontroller import ServerController
import os
import logging
import time

logger = logging.getLogger(__name__)


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
    parser.add_argument("-p", "--port", dest="port", required=True, type=int)
    args = parser.parse_args()
    configuration = yaml.load(args.filename.read())
    controller = ServerController(args.port)
    for _, attributes in configuration['nodes'].iteritems():
        logger.debug("Adding node")
        controller.cluster.add_node(attributes['username'], attributes['address'], attributes['port'])

    try:
        controller.start_server()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        controller.stop_server()
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.debug("%s" % e)
        sys.exit(-1)
