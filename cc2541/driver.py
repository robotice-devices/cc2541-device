import os
import six
import sys

import argparse
import optparse

# If ../cc2541/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                                os.pardir,
                                                os.pardir))
if os.path.exists(os.path.join(possible_topdir, 'cc2541', '__init__.py')):
    sys.path.insert(0, possible_topdir)

import argparse

from cc2541.sensor import get_data

parser = argparse.ArgumentParser(description='BLE Robotice Driver.')
parser.add_argument('address', nargs='?', help='Address')
parser.add_argument('-r', '--repeat', action='store_true', help="Repeat", default=False)

def pp(data):

    for datum in data:
        print str(datum)

def main():

    args = parser.parse_args()
    
    print(args)
    
    bluetooth_adr = getattr(args, "address", sys.argv[1]) 

    pp(get_data({"address":bluetooth_adr}))

    if args.repeat:

        while True:
            pp(get_data({"address":bluetooth_adr}))

if __name__ == "__main__":
    main()