###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###
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

def main():
    args = docopt(__doc__,version='dcos-oneview version {}'.format(constants.version), help=False)

    if args['--status']:
        oneview_service_client.get_status()

    elif args['--capacity']:
        oneview_service_client.get_capacity()

    elif args['--alive']:
        oneview_service_client.get_base_service()

    elif args['--addnode'] and args['--count']:
        print("Provision node ...")
        count = args["--count"]
        oneview_service_client.add_node(count)

    elif args['--removenode'] and args['--count']:
        print("Release node ...")
        count = args["--count"]
        oneview_service_client.remove_node(count)

    else:
        print(__doc__)
	return 1

    return 0

if __name__ == "__main__":
    main()
