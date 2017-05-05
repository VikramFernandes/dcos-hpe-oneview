"""DCOS OneView Example Subcommand

Usage:
    dcos-oneview --status
    dcos-oneview --capacity
    dcos-oneview --addnode --count=NO_OF_NODES
    dcos-oneview --removenode --count=NO_OF_NODES

Options:
    --help           Show this screen
    --version        Show version
"""

from docopt import docopt, DocoptExit
from dcos_oneview import oneview_service_client
from dcos_oneview import constants
import sys


def main():
    args = docopt(__doc__,version='dcos-oneview version {}'.format(constants.version), help=False)
    #print(args)

    if args['--status']:
        oneview_service_client.get_status()

    elif args['--capacity']:
        oneview_service_client.get_capacity()

    elif args['--addnode'] and args['--count']:
        #print("count : {count}".format(count=args["--count"]))
        print("Adding node ...")
        count = args["--count"]
        oneview_service_client.add_node(count)

    elif args['--removenode'] and args['--count']:
        #print("count : {count}".format(count=args["--count"]))
        print("Removing node ...")
        count = args["--count"]
        oneview_service_client.remove_node(count)

    else:
        print(__doc__)
	return 1

    return 0

if __name__ == "__main__":
    main()
